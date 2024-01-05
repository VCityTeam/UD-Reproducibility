# Reference: https://stackoverflow.com/questions/28885137/how-to-run-wget-inside-ubuntu-docker-image

FROM ubuntu:20.04
RUN  apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
WORKDIR /data
