import os
from datetime import datetime
import pytz
from ..minio_helper import MinioHelper
import logging
logging.getLogger().setLevel(logging.INFO)


PLACE_HOLDER_FILE = "locking.tmp"
TZ = "Asia/Ho_Chi_Minh"

def lock_repo(local_repo):
    path = os.path.join(local_repo, PLACE_HOLDER_FILE)
    if os.path.isfile(path):
        return False
    with open(path, "w") as f:
        pass
    return True
    

def unlock_repo(local_repo):
    path = os.path.join(local_repo, PLACE_HOLDER_FILE)
    try:
        os.remove(path)
    except OSError:
        pass
    
    
def get_localized_datetime(datetime_str=None):
    if datetime_str is None:
        return None
    
    # Define the timezone for Ho Chi Minh City
    hcm_timezone = pytz.timezone(TZ)
    
    # Convert the string to a naive datetime object
    try:
        naive_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        logging.error(e)
        return None

    # Localize the naive datetime object to the Ho Chi Minh timezone
    localized_datetime = hcm_timezone.localize(naive_datetime)
    return localized_datetime


def sync_repo_no_conflict(bucket_name, repo_prefix, local_repo, version_name=None):
    os.makedirs(local_repo, exist_ok=True)
    if not lock_repo(local_repo):
        logging.info("Another process is locking this repository, skip for now.")
        return False
    
    try:
        minio_helper = MinioHelper(
            url=os.environ["MINIO_URL"],
            access_key=os.environ["MINIO_ACCESS_KEY"],
            secret_key=os.environ["MINIO_SECRET_KEY"],
            secure=os.environ["MINIO_SECURE"].lower() == "true"
        )
        
        if version_name is None:
            logging.warning("Version is not provided, using the latest version.")
    
        logging.info("Synchronizing from remote to local...")
        minio_helper.synchronize_repo(
            bucket_name,
            repo_prefix,
            local_repo,
            version_name=version_name,
            pbar=True,
        )
    except Exception as e:
        raise e
    finally:
        unlock_repo(local_repo)
    
    logging.info("Successfully synchronized repository!")
    return True


def upload_repo(bucket_name, repo_prefix, local_repo, version_name):
    minio_helper = MinioHelper(
        url=os.environ["MINIO_URL"],
        access_key=os.environ["MINIO_ACCESS_KEY"],
        secret_key=os.environ["MINIO_SECRET_KEY"],
        secure=os.environ["MINIO_SECURE"].lower() == "true"
    )

    logging.info("Uploading local repository...")
    minio_helper.upload_repo(bucket_name, repo_prefix, local_repo, version_name, pbar=True)
    logging.info("Successfully uploaded repository!")
    
    return True