#!/usr/bin/bash

vm1=$1
vm2=$2
zone=$3

echo "Checking Firewall Rules!!"
echo " "
gcloud compute ssh ${vm1}  --zone ${zone} --command "ping -w3 ${vm2}"
echo " "
echo "ping is Successful from $vm1 to $vm2!!"
