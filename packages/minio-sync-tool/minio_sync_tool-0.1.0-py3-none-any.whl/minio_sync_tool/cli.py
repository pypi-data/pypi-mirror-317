import argparse
from .tasks import sync_repo_no_conflict, upload_repo

def main():
    parser = argparse.ArgumentParser(
        description="CLI tools for interacting with MinIO for repository synchronization and upload."
    )
    
    subparsers = parser.add_subparsers(
        title="commands",
        description="Available commands",
        dest="command"
    )
    
    # Sync Command
    sync_parser = subparsers.add_parser(
        "sync_repo", 
        help="Synchronize a repository from MinIO to local storage."
    )
    sync_parser.add_argument(
        "--bucket", 
        required=True, 
        help="Name of the MinIO bucket containing the repository."
    )
    sync_parser.add_argument(
        "--prefix", 
        required=True, 
        help="Prefix (folder path) in the bucket to sync."
    )
    sync_parser.add_argument(
        "--dest", 
        required=True, 
        help="Local directory where the repository will be synchronized."
    )
    sync_parser.add_argument(
        "--version", 
        default=None, 
        help="Version of the repository to sync."
    )
    
    # Upload Command
    upload_parser = subparsers.add_parser(
        "upload_repo", 
        help="Upload a repository from local storage to MinIO."
    )
    upload_parser.add_argument(
        "--bucket", 
        required=True, 
        help="Name of the MinIO bucket where the repository will be uploaded."
    )
    upload_parser.add_argument(
        "--prefix", 
        required=True, 
        help="Prefix (folder path) in the bucket to upload to."
    )
    upload_parser.add_argument(
        "--source", 
        required=True, 
        help="Local directory containing the repository to upload."
    )
    upload_parser.add_argument(
        "--version", 
        required=True, 
        help="Version name of the repository."
    )
    
    args = parser.parse_args()
    
    if args.command == "sync_repo":
        sync_repo_no_conflict(
            bucket_name=args.bucket,
            repo_prefix=args.prefix,
            local_repo=args.dest,
            version_name=args.version,
        )
    elif args.command == "upload_repo":
        upload_repo(
            bucket_name=args.bucket,
            repo_prefix=args.prefix,
            local_repo=args.source,
            version_name=args.version,
        )
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
