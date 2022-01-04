#!/usr/bin/env python3

import os
import boto3
from botocore.exceptions import ClientError

ACCESS_KEY = 'AWS_ACCESS_KEY_ID'
SECRET_SECRET_KEY = 'AWS_SECRET_ACCESS_KEY_ID'
PRI_BUCKET_NAME = 'python-tutorials-bucket'
TRANSIENT_BUCKET_NAME = 'python-tutorials-bucket2'
FILE_1 = 'test_file.txt'
FILE_2 = 'test_file_2.txt'
DIR = '/workspaces/python_tutorials'
DOWN_DIR = '/workspaces/python_tutorials'

def main():
    print('AWS S3 ACCESS')
    access_key = os.getenv(ACCESS_KEY)
    secret_access_key = os.getenv(SECRET_SECRET_KEY)
    s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
    #create_bucket(TRANSIENT_BUCKET_NAME, s3)
    #download_file(PRI_BUCKET_NAME, DOWN_DIR, FILE_1, FILE_1, s3)
    #upload_file(TRANSIENT_BUCKET_NAME, DIR, FILE_1, s3)
    #delete_file(TRANSIENT_BUCKET_NAME, [FILE_1], s3)
    #copy_file(PRI_BUCKET_NAME, TRANSIENT_BUCKET_NAME, FILE_1, FILE_2, s3)
    #list_objects(TRANSIENT_BUCKET_NAME, s3)
    #prevent_public_access(TRANSIENT_BUCKET_NAME, s3)
    #generate_download_link(TRANSIENT_BUCKET_NAME, FILE_1, 60, s3)
    delete_bucket(TRANSIENT_BUCKET_NAME, s3)


def upload_file(bucket, directory, file, s3, s3path=None):
    file_path = directory + '/' + file
    remote_path = s3path
    if remote_path is None:
        remote_path = file
    try:
        s3.Bucket(bucket).upload_file(file_path, remote_path)
    except ClientError as ce:
        print('error', ce)


def download_file(bucket, directory, local_name, key_name, s3):
    file_path = directory + '/' + local_name
    try:
        s3.Bucket(bucket).download_file(key_name, file_path)
    except ClientError as ce:
        print('error', ce)


def delete_file(bucket, keys, s3):
    objects = []
    for key in keys:
        objects.append({'Key' : key})
    try:
        s3.Bucket(bucket).delete_objects(Delete={'Objects': objects})
    except ClientError as ce:
        print('error', ce)

    
def list_objects(bucket, s3):
    try:
        response = s3.meta.client.list_objects(Bucket=bucket)
        objects = []
        for content in response['Contents']:
            objects.append(content['Key'])
        print(bucket, 'contains', len(objects), 'files')
        return objects
    except ClientError as ce:
        print('error', ce)


def copy_file(source_bucket, destination_bucket, source_key, destination_key, s3):
    try:
        source = {
            'Bucket': source_bucket,
            'Key': source_key
        }
        s3.Bucket(destination_bucket).copy(source, destination_key)
    except ClientError as ce:
        print('error', ce)


def prevent_public_access(bucket, s3):
    try:
        s3.meta.client.put_public_access_block(Bucket=bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True,
            })
    except ClientError as ce:
        print('error', ce)


def generate_download_link(bucket, key, expiration_seconds, s3):
    try:
        response = s3.meta.client.generate_presigned_url('get_object', Params={
            'Bucket': bucket,
            'Key': key
        }, ExpiresIn=expiration_seconds)
        print(response)
    except ClientError as ce:
        print('error', ce)


def create_bucket(name, s3):
    try:
        bucket = s3.create_bucket(Bucket=name)
    except ClientError as ce:
        print('error', ce)


def delete_bucket(bucket, s3):
    try:
        s3.Bucket(bucket).delete()
    except ClientError as ce:
        print('error', ce)


if __name__ == '__main__':
    main()
