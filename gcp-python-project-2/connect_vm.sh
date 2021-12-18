#!/usr/bin/bash

vm1=$1
vm2=$2
zone=$3

gcloud compute ssh ${vm1}  --zone ${zone} --command "ping -w3 ${vm2}"
