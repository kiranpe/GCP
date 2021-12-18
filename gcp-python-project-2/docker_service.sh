#!/usr/bin/bash
sym_link='/etc/systemd/system/multi-user.target.wants/docker.service'
host=$1

echo "Checking Docker Service Status on $host!!"

if [ -L $sym_link ];then
  echo "Docker Service Enabled on $host!!"
else
  echo "Docker Service is Disabled on $host . Enabling it!!" 
  sudo systemctl enable docker
fi
