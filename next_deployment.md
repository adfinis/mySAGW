# Manual steps for next deployment

## MinIO

The intermediate containers for the storage backend migration can be removed:

 - `minio-legacy`
 - `minio-migrate`

The volume `minio-data` can be removed.
