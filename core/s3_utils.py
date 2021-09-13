# helper functions for files on s3 and compatible object storage service
# can draw inspiration from:
# https://github.com/Mashoud123/Python3-DigitalOcean-Spaces-Manager-v2-Advanced/blob/master/spaces.py

from django.conf    import settings

import boto3

from botocore.client import Config


sBucketName = settings.AWS_STORAGE_BUCKET_NAME


def getClient():
    #
    oSession = boto3.session.Session()
    #
    client = oSession.client(
            's3',
            region_name             = settings.AWS_S3_ENDPOINT_URL[8:12],
            endpoint_url            = settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id       = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key   = settings.AWS_SECRET_ACCESS_KEY )
    #
    return client

def _getPaginator():
    #
    s3_paginator = boto3.client(
            's3',
            region_name             = settings.AWS_S3_ENDPOINT_URL[8:12],
            endpoint_url            = settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id       = settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key   = settings.AWS_SECRET_ACCESS_KEY,
            config                  = Config(
                                    s3 = { 'addressing_style': 'virtual' } )
        ).get_paginator('list_objects_v2')
    #
    return s3_paginator

def getFileNameGenerator(
        bucket_name = sBucketName,
        prefix      = '/',
        delimiter   = '/',
        start_after = '' ):
    #
    prefix = prefix[1:] if prefix.startswith(delimiter) else prefix
    start_after = (start_after or prefix) if prefix.endswith(delimiter) else start_after
    #
    s3_paginator = _getPaginator()
    #
    for page in s3_paginator.paginate(
            Bucket      = bucket_name,
            Prefix      = prefix,
            StartAfter  = start_after):
        for content in page.get('Contents', ()):
            yield content['Key']


def getFileList(
        bucket_name = sBucketName,
        prefix      = '/',
        delimiter   = '/',
        start_after = '' ):
    #
    return list(
            getFileNameGenerator(
                bucket_name, prefix, delimiter, start_after ) )

def putFile( sLocalFile, sUploadName ):
    #
    try:
        #
        oClient = getClient()
        #
        oClient.upload_file( sLocalFile, sBucketName, sUploadName )
        #
        message = 'success'
        #
    except Exception as e:
        #
        message = 'error: %s' % str( e )
        #
    return message

