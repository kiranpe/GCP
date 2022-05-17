#!/usr/bin/env python3
import os
import sys
from google.cloud import storage

def ods_seg_cloud_function(event, context):
    print('Event type: {}'.format(context.event_type))
    print('Bucket: {}'.format(event['bucket']))
    print('File: {}'.format(event['name']))

    blob_name = event['name']
    bucket_name = event['bucket']
    destination_blob_name = event['name']
    destination_bucket_name = "test1-bucket-kiran"

    storage_client = storage.Client()
    source_bucket = storage_client.bucket(bucket_name)
    source_blob = source_bucket.blob(blob_name)
    destination_bucket = storage_client.bucket(destination_bucket_name)

    blob_copy = source_bucket.copy_blob(
      source_blob, destination_bucket, destination_blob_name
    )

    print(f"Blob {source_blob.name} in bucket {source_bucket.name} copied to blob {blob_copy.name} in bucket {destination_bucket.name}.")
    return "Copied files Successfully!!"
