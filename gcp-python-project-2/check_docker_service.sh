#!/usr/bin/bash

function print_color(){
  NC='\033[0m' # No Color

  case $1 in
    "green") COLOR='\033[0;32m' ;;
    "red") COLOR='\033[0;31m' ;;
    "*") COLOR='\033[0m' ;;
  esac

  echo -e "${COLOR} $2 ${NC}"
}

username="kiranpeddineni"
project=$1
zone=$2
vm=$3

gcloud compute scp --project $project --zone $zone docker_service.sh ${username}@${vm}:/tmp > /dev/null 2>&1

gcloud compute ssh $vm --zone $zone --command "/tmp/docker_service.sh $vm" 2> /dev/null

if [ $? != 0 ];then
  print_color "red" "Not able to Connect to Server $vm!!"
fi
