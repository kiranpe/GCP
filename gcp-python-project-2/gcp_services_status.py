#!/usr/bin/env python3
import os
import json
import sys
import subprocess
import urllib.request
import requests
import emoji
from rich.console import Console
from rich.theme import Theme
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
 
destination_blob_name = os.popen("""cat main.tf | grep file_name | awk -F"=" '{print $2}' | tr -d '"' | sed 's/^ //g'""").read().strip()
source_file_name = os.popen("""cat main.tf | grep file_name | awk -F"=" '{print $2}' | tr -d '"' | sed 's/^ //g'""").read().strip()

instances = [vm1, vm2]

storage_client = storage.Client()
custom_theme = Theme({"status": "yellow", "success": "green", "error": "bold red"})
console = Console(theme=custom_theme)

credentials = service_account.Credentials.from_service_account_file(
        filename=os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
        scopes=['https://www.googleapis.com/auth/cloud-platform'])

service = discovery.build('compute', 'beta', credentials=credentials)

def list_service_accounts(project_id):
  service = discovery.build('iam', 'v1', credentials=credentials)

  service_accounts = service.projects().serviceAccounts().list(
     name='projects/' + project_id).execute()

  for account in service_accounts['accounts']:
     if account['displayName'] in 'readaccess':
       console.print(":thumbs_up: Service Account | {} | [success]Exists![/success]\n".format(account['name']))

list_service_accounts(projectId)

def check_bucket():
    bucket = storage_client.get_bucket(bucket_name)
    if bucket.name in bucket_name:
      console.print(":thumbs_up: Bucket | {} | [success]Exists![/success]\n".format(bucket.name)) 
    else:
      print(":thumbs_down: Bucket | {} | [error]Doesn't Exists![/error]\n".format(bucket.name))

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
    console.print(":thumbs_up: file: {} uploaded to bucket: {} | [success]Successful[/success]\n".format(source_file_name,bucket.name))
  except Exception as e:
    console.print(":thumbs_down: file: {} upload to bucket: {} | Failed".format(source_file_name,bucket.name), style="error")
    if e.code == 403:
      console.print(" ⚠️  Service Account {} does not have storage.objects.create access to the 🪣  bucket: {}\n".format(sa,bucket.name))
 
upload_file()

def instance_status():
  for instance_name in instances:
    response = service.instances().get(project=projectId, zone=zone, instance=instance_name).execute()
    if response['status'] in 'RUNNING':
     console.print(":thumbs_up: {} | status | [success]{}[/success]\n".format(instance_name,response['status']))
    else:
     console.print(":thumbs_down: {} | status | [error]{}[/error]\n".format(instance_name,response['status']))
   
instance_status()

def ping_instance():
  try:
    subprocess.call(['bash', './ping_test.sh', instances[0], instances[1], zone])
    print(" ")
  except:
    print(" ")

ping_instance()

def check_docker_service():
 for vm in instances:
  try:
   subprocess.call(['bash', './check_docker_service.sh', projectId, zone, vm])
   print(" ")
  except:
    print("Script is Failed!! Check script once!!\n")
 
check_docker_service()

def container_status():
 ips = []

 try: 
   for instance_name in instances:
     response = service.instances().get(project=projectId, zone=zone, instance=instance_name).execute()
     ips.append(response['networkInterfaces'][0]['accessConfigs'][0]['natIP'])
 except:
   console.print(":thumbs_down: [error]{} Server is NOT RUNNING!! Not able to get IP Address!![/error]\n".format(instance_name))

 for host in ips:
  container_urls = ["http://" +host+ ":10800" +"/index.html", "http://" +host+ ":10801" +"/index.html"]
  console.print("[status]Checking Container Status on {}!![/status]".format(host))
  for url in container_urls:
   try:
     response = requests.get(url)
     if response.status_code == 200:
       if urlparse(url).port == 10800:
         console.print("✅ [success]Nginx Container is Up and Running on host:[/success] {}\n".format(host))
       else:
         console.print("✅ [success]Apache Container is Up and Running on host:[/success] {}\n".format(host))
   except:
     if urlparse(url).port == 10800:
       console.print("❌ [error]Nginx Container on host:[/error] {} [error]is not running. Please check.[/error]\n".format(host))
     else:
       console.print("❌ [error]Apache Container on host:[/error] {} [error]is not running. Please check.[/error]\n".format(host))

container_status()

console.print("Script is completed!! If Any Queries reach out to Kiran Peddineni 👨‍💻 !!", style="bold")
