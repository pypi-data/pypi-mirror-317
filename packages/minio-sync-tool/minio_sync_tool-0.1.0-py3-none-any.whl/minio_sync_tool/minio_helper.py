import logging
import os
import tqdm
from datetime import datetime
import pytz

from minio import Minio, S3Error
from minio.versioningconfig import VersioningConfig, ENABLED
from minio.helpers import get_part_info
from minio.commonconfig import Tags
from .utils import calculate_multipart_etag


REPO_VERSION_KEY = "version"
REPO_TIMESTAMP_KEY = "timestamp"
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

class MinioHelper:
    def __init__(
        self,
        url,
        access_key,
        secret_key,
        secure=True,
    ):
        self.client = Minio(
            endpoint=url,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
        )
        
    def make_bucket_with_versioning(self, bucket_name):
        self.client.make_bucket(bucket_name)
        self.client.set_bucket_versioning(bucket_name, VersioningConfig(ENABLED))
        
    def list_repo_objects(self, bucket_name, prefix=None, *args, **kwargs):
        objs = self.client.list_objects(bucket_name, prefix=prefix, *args, **kwargs)
        for obj in objs:
            if not os.path.relpath(obj.object_name, prefix).startswith(".."):
                yield obj
        
    def get_object_versions(self, bucket_name, object_name):
        return self.list_repo_objects(bucket_name, prefix=object_name, include_version=True)
    
    def get_version_at_timepoint(self, bucket_name, object_name, timepoint: datetime):
        versions = self.get_object_versions(bucket_name, object_name)
        versions = [obj for obj in versions if obj.last_modified <= timepoint]
        if versions:
            version = max(versions, key=lambda obj: obj.last_modified)
            return None if version.is_delete_marker else version.version_id
        else:
            return None
        
    def get_repo_latest_version(self, bucket_name, repo_prefix):
        objs = self.list_repo_objects(bucket_name, prefix=repo_prefix, recursive=True, include_version=True)
        objs = [obj for obj in objs if not obj.is_delete_marker]
        all_tags = []
        for obj in objs:
            tags = self.client.get_object_tags(bucket_name, obj.object_name, obj.version_id)
            if tags is not None:
                all_tags.append(tags)
        if not all_tags:
            return None
            
        def compare_func(tags):
            try:
                datetime_str = tags[REPO_TIMESTAMP_KEY]
                return datetime.strptime(datetime_str, TIMESTAMP_FORMAT)
            except Exception as e:
                logging.error(e)
                return datetime.min
            
        latest_tags = max(all_tags, key=compare_func)
        return latest_tags[REPO_VERSION_KEY]
    
    def list_repo_objects_by_version(self, bucket_name, repo_prefix, version_name):
        objs = self.list_repo_objects(bucket_name, prefix=repo_prefix, recursive=True, include_version=True)
        objs = [obj for obj in objs if not obj.is_delete_marker]
        res_objs = []
        for obj in objs:
            tags = self.client.get_object_tags(bucket_name, obj.object_name, obj.version_id)
            if tags is not None and tags[REPO_VERSION_KEY] == version_name:
                res_objs.append(obj)
        
        return res_objs
                
    def list_repo_objects_at_timepoint(self, bucket_name, repo_prefix, timepoint: datetime):
        objs = self.list_repo_objects(bucket_name, prefix=repo_prefix, recursive=True, include_version=True)
        objs = [obj for obj in objs if obj.last_modified <= timepoint]
        objs = sorted(objs, key=lambda obj: obj.last_modified, reverse=True)
        names = set()
        res_objs = []
        for obj in objs:
            if obj.object_name not in names:
                res_objs.append(obj)
                names.add(obj.object_name)
                
        # Get rid of deleted objects
        res_objs = [obj for obj in res_objs if not obj.is_delete_marker]
        return res_objs
    
    def _checksum_object(self, bucket_name, object_name, local_object, version_id=None):
        file_length = os.path.getsize(local_object)
        part_size, part_count = get_part_info(file_length, 0)
        
        local_md5 = calculate_multipart_etag(local_object, part_size)
        obj = self.client.stat_object(bucket_name, object_name, version_id=version_id)
        md5 = obj.etag
        if md5 != local_md5:
            return False
        return True
    
    def synchronize_object(self, bucket_name, object_name, local_object, version_id=None):
        # Sync from remote to local
        if not os.path.exists(local_object) or not self._checksum_object(bucket_name, object_name, local_object, version_id=version_id):
            self.client.fget_object(bucket_name, object_name, local_object, version_id=version_id)
            
    def synchronize_repo(self, bucket_name, repo_prefix, local_repo, version_name=None, pbar=False):
        if version_name is None:
            version_name = self.get_repo_latest_version(bucket_name, repo_prefix)
        
        remote_objs = self.list_repo_objects_by_version(bucket_name, repo_prefix, version_name)
        if not remote_objs:
            raise ValueError("Version does not exist.")
        
        version_ids = [obj.version_id for obj in remote_objs]
        remote_paths = [obj.object_name for obj in remote_objs]
        rel_paths = [os.path.relpath(path, repo_prefix) for path in remote_paths]
        local_paths = [os.path.join(local_repo, path) for path in rel_paths]
        
        if pbar:
            progress_bar = tqdm.tqdm(total=len(remote_paths))
        for rem_obj, loc_obj, version_id in zip(remote_paths, local_paths, version_ids):
            self.synchronize_object(bucket_name, rem_obj, loc_obj, version_id=version_id)
            if pbar:
                progress_bar.update(1)
        
    def upload_repo(self, bucket_name, repo_prefix, local_repo, version_name, pbar=False):
        # Validate and check if version exists
        if not isinstance(version_name, str) or not version_name:
            raise ValueError("Invalid version name.")
        if self.list_repo_objects_by_version(bucket_name, repo_prefix, version_name):
            raise ValueError("Version exists.")
        
        local_paths = []
        for root, dirs, files in os.walk(local_repo):
            for file in files:
                local_paths.append(os.path.join(root, file))
        
        rel_paths = [os.path.relpath(path, local_repo) for path in local_paths]
        remote_paths = [os.path.join(repo_prefix, path) for path in rel_paths]
        
        version_tags = Tags.new_object_tags()
        version_tags[REPO_VERSION_KEY] = version_name
        version_tags[REPO_TIMESTAMP_KEY] = datetime.now().strftime(TIMESTAMP_FORMAT)
        
        if pbar:
            progress_bar = tqdm.tqdm(total=len(remote_paths))
        for rem_obj, loc_obj in zip(remote_paths, local_paths):
            self.client.fput_object(bucket_name, rem_obj, loc_obj, tags=version_tags)
            if pbar:
                progress_bar.update(1)
