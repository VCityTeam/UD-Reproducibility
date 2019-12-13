#!/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi
apt-get install -y apache2

# npm version 6.11.3 (Ubuntu 18.04)
# Reference: https://linuxize.com/post/how-to-install-node-js-on-ubuntu-18.04/
apt install -y curl
curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
sudo apt-get install -y nodejs

