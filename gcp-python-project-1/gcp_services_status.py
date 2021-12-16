#!/usr/bin/env python3
import os
import json
import sys
from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient import discovery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/kiran/devops/GCP/credentials.json"

storage_client = storage.Client()
projectId = "pythonproject-335216"
bucket_name = "kiran-python-project-1"
destination_blob_name = 'dummy.txt'
source_file_name = 'dummy.txt'
zone = 'us-west4-b'
instances = ['vm-0','vm-1']

def list_service_accounts(project_id):
  credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

  service = discovery.build(
        'iam', 'v1', credentials=credentials)

  service_accounts = service.projects().serviceAccounts().list(
        name='projects/' + project_id).execute()

  for account in service_accounts['accounts']:
        if account['displayName'] in 'readaccess':
           print("Service Account | {} | Exists".format(account['name']))
           print(" ")

list_service_accounts(projectId)

def check_bucket():
    bucket = storage_client.get_bucket(bucket_name)
    if bucket.name in 'kiran-python-project-1':
      print("Bucket | {} | Exists".format(bucket.name)) 
      print(" ")
    else:
      print("Bucket | {} | Not Exists".format(bucket.name))
      print(" ")

check_bucket()

def upload_file():
  client = storage.Client.from_service_account_json(json_credentials_path='credentials.json')
  bucket = client.get_bucket(bucket_name)

  try:
 
    object_name_in_gcs_bucket = bucket.blob(destination_blob_name)
    object_name_in_gcs_bucket.upload_from_filename(source_file_name)
    print('file: ',source_file_name,' uploaded to bucket: ',bucket,' successfully')
    print(" ")
    print(" ")

  except Exception as e:
    print("file: {} upload to bucket: {} | Failed".format(source_file_name,bucket.name))
    if e.code == 403:
      print("Service Account does not have storage.objects.create access to the Google Cloud Storage object.")
    print(" ")
    print(" ")
 
upload_file()

def instance_status():
  credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

  service = discovery.build('compute', 'beta', credentials=credentials)

  for instance_name in instances:
      request = service.instances().get(project=projectId, zone=zone, instance=instance_name)
      response = request.execute()
      print("{} | status | {}".format(instance_name,response['status']))
      print(" ")
      
instance_status()

def ping_instance():
  COMMAND='/home/kiran/devops/GCP/google-cloud-sdk/bin/gcloud compute ssh vm-0 --zone=us-west4-b --command="ping -w3 vm-1"'

  print("Checking Firewall Rules!!")
  result = os.system(COMMAND)

  if result == []:
    error = ssh.stderr.readlines()
    print >>sys.stderr, "ERROR: %s" % error
  else:
    print(" ")
    print("Ping is Successful from VM-0 to VM-1!!") 

ping_instance()
