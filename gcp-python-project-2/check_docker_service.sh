#!/usr/bin/bash
username="kiranpeddineni"
project=$1
zone=$2
vm=$3

gcloud compute scp --project $project --zone $zone docker_service.sh ${username}@${vm}:/tmp > /dev/null 2>&1

gcloud compute ssh $vm --zone $zone --command "/tmp/docker_service.sh $vm" 2> /dev/null

if [ $? != 0 ];then
  echo "Not able to Connect to Server $vm!!"
fi
