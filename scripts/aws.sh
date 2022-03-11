#!/bin/sh
sudo yum update -y
sudo amazon-linux-extras install docker
sudo usermod -a -G docker ec2-user
docker run -p 80:3000 benjaminkrueger/2022-kringlecon
