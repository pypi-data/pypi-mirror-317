# MinIO Sync Tool

MinIO Sync Tool is a Python package that simplifies repository synchronization and uploads between local storage and MinIO. It provides an easy-to-use command-line interface for managing files in MinIO buckets.

---

## Features

- Synchronize a repository from MinIO to local storage.
- Upload a repository from local storage to MinIO.
- Command-line interface for quick and easy usage.

---

## Usage

The package provides a CLI tool called sync_minio_repo with the following commands:

### Environment

```bash
export MINIO_URL=...
export MINIO_ACCESS_KEY=...
export MINIO_SECRET_KEY=...
export MINIO_SECURE=false # true/false
```

### Synchronize Repository from MinIO to Local

```bash
minio_sync_tool sync_repo \
    --bucket my-bucket \
    --prefix my-repo/ \
    --dest ./local-repo \
    --version "version-name"
```

**Arguments:**

* `--bucket`: Name of the MinIO bucket containing the repository.

* `--prefix`: Prefix (folder path) in the bucket to sync.

* `--dest`: Local directory where the repository will be synchronized.

* `--version`: Version of the repository to sync.

### Upload Repository from Local to MinIO

```bash
minio_sync_tool upload_repo \
    --bucket my-bucket \
    --prefix my-repo/ \
    --source ./local-repo
    --version "version-name"
```

**Arguments:**

* `--bucket`: Name of the MinIO bucket where the repository will be uploaded.

* `--prefix`: Prefix (folder path) in the bucket to upload to.

* `--source`: Local directory containing the repository to upload.

* `--version`: Version name of the repository.
