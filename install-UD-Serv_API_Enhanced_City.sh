#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

apt-get install docker
apt-get install docker-compose
systemctl start docker.service

## This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# Refer to https://github.com/MEPP-team/UD-Serv/blob/master/API_Enhanced_City/INSTALL.md#install-using-docker

cd Services
git clone https://github.com/MEPP-team/UD-Serv.git
cd UD-Serv/API_Enhanced_City
docker-compose build
docker-compose up &
