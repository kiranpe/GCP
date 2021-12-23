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

sym_link='/etc/systemd/system/multi-user.target.wants/docker.service'
host=$1

echo "Checking Docker Service Status on $host!!"

if [ -L $sym_link ];then
  print_color "green" "Docker Service Enabled on $host!!"
else
  print_color "red" "Docker Service is Disabled on $host . Enabling it!!" 
  sudo systemctl enable docker
fi
