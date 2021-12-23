#!/usr/bin/bash

function print_color(){
  NC='\033[0m' # No Color

  case $1 in
    "yellow") COLOR='\033[0;33m' ;;
    "green") COLOR='\033[0;32m' ;;
    "red") COLOR='\033[0;31m' ;;
    "*") COLOR='\033[0m' ;;
  esac

  echo -e "${COLOR} $2 ${NC}"
}

function ping(){
  vm1=$1
  vm2=$2
  zone=$3

  print_color "yellow" "Checking Firewall Rules!!"

  ping_test=$(gcloud compute ssh ${vm1}  --zone ${zone} --command "ping -w3 ${vm2}")

  if [ $? = 0 ];then
    echo " "
    print_color "green" "ping is Successful from $vm1 to $vm2!!"
  else
    echo " "
    print_color "red" "Ping is Failing from $vm1 to $vm2!!"
  fi
}

ping $1 $2 $3
