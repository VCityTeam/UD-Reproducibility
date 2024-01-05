# Reference: https://stackoverflow.com/questions/28885137/how-to-run-wget-inside-ubuntu-docker-image

FROM ubuntu:20.04
RUN  apt-get update \
  && apt-get install -y patch \
  && rm -rf /var/lib/apt/lists/*
COPY Exp-Cloud-ELAPHS-94M-3DTiles-Lyon.patch Exp-Cloud-ELAPHS-94M-3DTiles-Lyon.patch
COPY patch_tileset.sh patch_tileset.sh
RUN chmod a+x /patch_tileset.sh
ENTRYPOINT ["/patch_tileset.sh"]
