from storages.backends.s3boto3 import S3Boto3Storage

class CustomStorage( S3Boto3Storage ):
    bucket_name = 'auction-files'
    default_acl = 'public-read'

class StaticStorage( CustomStorage ):
    location    = 'static'

class MediaStorage( CustomStorage ):
    location    = 'media'
