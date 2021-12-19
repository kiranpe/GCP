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

with open("terraform.tfstate") as file:
  data = json.load(file)

  projectId = (data['resources'][0]['instances'][0]['attributes']['project'])
  zone = (data['resources'][3]['instances'][0]['attributes']['zone'])
  bucket_name = (data['resources'][10]['instances'][0]['attributes']['name'])
  vm1 = (data['resources'][3]['instances'][0]['attributes']['name'])
  vm2 = (data['resources'][3]['instances'][1]['attributes']['name'])
 
destination_blob_name = os.popen("""cat terraform.tfvars | grep file_name | awk -F"=" '{print $2}' | tr -d '"' | sed 's/^ //g'""").read().strip()
source_file_name = os.popen("""cat terraform.tfvars | grep file_name | awk -F"=" '{print $2}' | tr -d '"' | sed 's/^ //g'""").read().strip()

instances = [vm1, vm2]

storage_client = storage.Client()

credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

def list_service_accounts(project_id):
  service = discovery.build('iam', 'v1', credentials=credentials)

  service_accounts = service.projects().serviceAccounts().list(
     name='projects/' + project_id).execute()

  for account in service_accounts['accounts']:
     if account['displayName'] in 'readaccess':
       print("Service Account | {} | Exists".format(account['name']))
       print(" ")

list_service_accounts(projectId)

def check_bucket():
    bucket = storage_client.get_bucket(bucket_name)
    if bucket.name in bucket_name:
      print("Bucket | {} | Exists".format(bucket.name)) 
      print(" ")
    else:
      print("Bucket | {} | Not Exists".format(bucket.name))
      print(" ")

check_bucket()

def upload_file():
  with open("credentials.json") as file:
    data = json.load(file)
    sa = data["client_email"]
  client = storage_client.from_service_account_json(json_credentials_path='credentials.json')
  bucket = client.get_bucket(bucket_name)

  try:
    object_name_in_gcs_bucket = bucket.blob(destination_blob_name)
    object_name_in_gcs_bucket.upload_from_filename(source_file_name)
    print('file: ',source_file_name,' uploaded to bucket: ',bucket.name,' successfully')
    print(" ")
  except Exception as e:
    print("file: {} upload to bucket: {} | Failed".format(source_file_name,bucket.name))
    if e.code == 403:
      print("Service Account {} does not have storage.objects.create access to the bucket: {}".format(sa,bucket.name))
      print(" ")
 
upload_file()

def instance_status():
  service = discovery.build('compute', 'beta', credentials=credentials)

  for instance_name in instances:
    response = service.instances().get(project=projectId, zone=zone, instance=instance_name).execute()
    print("{} | status | {}".format(instance_name,response['status']))
    print(" ")
   
instance_status()

def ping_instance():
  try:
    subprocess.call(['sh', './ping_test.sh', instances[0], instances[1], zone])
    print(" ")
  except:
    print(" ")

ping_instance()

def check_docker_service():
 for vm in instances:
  try:
   subprocess.call(['sh', './check_docker_service.sh', projectId, zone, vm])
   print(" ")
  except:
    print("Script is Failed!! Check script once!!")
 
check_docker_service()

def container_status():
 ips = []

 try: 
   service = discovery.build('compute', 'beta', credentials=credentials)
   for instance_name in instances:
     response = service.instances().get(project=projectId, zone=zone, instance=instance_name).execute()
     ips.append(response['networkInterfaces'][0]['accessConfigs'][0]['natIP'])
 except:
   print("{} Server is NOT RUNNING!! Not able to get IP Address!!".format(instance_name))
   print("")

 for host in ips:
  container_urls = ["http://" +host+ ":10800" +"/index.html", "http://" +host+ ":10801" +"/index.html"]
  print("Checking Container Status on {}!!".format(host))
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
