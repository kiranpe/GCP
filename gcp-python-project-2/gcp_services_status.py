#!/usr/bin/env python3
import os
import json
import sys
import subprocess
import urllib.request
import requests
from urllib.parse import urlparse
from google.cloud import storage
from google.oauth2 import service_account
from googleapiclient import discovery

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/kiran/devops/GCP/credentials.json"

projectId = os.popen("""cat terraform.tfvars | grep projectId | awk -F"=" '{print $2}' | tr -d '"' | sed 's/^ //g'""").read().strip()
bucket_name = sys.argv[1]
destination_blob_name = os.popen("""cat terraform.tfvars | grep file_name | awk -F"=" '{print $2}' | tr -d '"' | sed 's/^ //g'""").read().strip()
source_file_name = os.popen("""cat terraform.tfvars | grep file_name | awk -F"=" '{print $2}' | tr -d '"' | sed 's/^ //g'""").read().strip()
zone = os.popen("""cat terraform.tfvars | grep zone | awk -F"=" '{print $2}' | tr -d '"' | sed 's/^ //g'""").read().strip()
instances = [sys.argv[2], sys.argv[3]]

storage_client = storage.Client()

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
    if bucket.name in sys.argv[1]:
      print("Bucket | {} | Exists".format(bucket.name)) 
      print(" ")
    else:
      print("Bucket | {} | Not Exists".format(bucket.name))
      print(" ")

check_bucket()

def upload_file():
  client = storage_client.from_service_account_json(json_credentials_path='credentials.json')
  bucket = client.get_bucket(bucket_name)

  try:
 
    object_name_in_gcs_bucket = bucket.blob(destination_blob_name)
    object_name_in_gcs_bucket.upload_from_filename(source_file_name)
    print('file: ',source_file_name,' uploaded to bucket: ',bucket.name,' successfully')
    print(" ")
    print(" ")

  except Exception as e:
    print("file: {} upload to bucket: {} | Failed".format(source_file_name,bucket.name))
    if e.code == 403:
      print("Service Account does not have storage.objects.create access to the bucket: {}".format(bucket.name))
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
  print("Checking Firewall Rules!!")
  try:
    subprocess.call(['sh', './connect_vm.sh', instances[0], instances[1], zone])
    print(" ")
    print("Ping is Successful from {} to {}!!".format(vm1,vm2)) 
    print(" ")
  except:
    print("Ping is Failing from {} to {}!!".format(vm1,vm2))
    print(" ")

ping_instance()

def check_docker_service():
 vm_zone=zone
  
 print("Checking Docker Service Status!!")
 for vm in instances:
  try:
   subprocess.call(['sh', './check_docker_service.sh', projectId, vm_zone, vm])
   print(" ")
  except:
   print("Script is Failed!! Check script once!!")
 
check_docker_service()

def container_status():
 ips = [sys.argv[4]]

 for host in ips:
  container_urls = ["http://" +host+ ":10800" +"/index.html", "http://" +host+ ":10801" +"/index.html"]
  
  print("Checking Container Status Now on {}!!".format(host))
  for url in container_urls:
   try:
     response = requests.get(url)

     if response.status_code == 200:
       if urlparse(url).port == 10800:
         print("Nginx Container is Up and Running on host: {}".format(host))
         print(" ")
       else:
         print("Apache Container is Up and Running on host: {}".format(host))
         print(" ")
   except:
     if urlparse(url).port == 10800:
       print("Nginx Container on host: {} is not running. Please check.".format(host))
       print(" ")
     else:
       print("Apache Container on host: {} is not running. Please check.".format(host))
       print(" ")

container_status()
