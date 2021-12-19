#!/usr/bin/bash

#Install docker
sudo apt-get update && sudo apt install docker.io -y

#Enable docker service
sudo systemctl enable docker

#Add docker to current user
sudo usermod -aG docker $USER

#Pull Docker images

for image in nginx httpd
do
sudo docker pull $image
done

#Run images
sudo docker run -it --name nginx -p 10800:80 -d nginx

sudo docker run -it --name apache -p 10801:80 -d httpd
