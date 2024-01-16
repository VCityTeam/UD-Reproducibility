# Reference: https://stackoverflow.com/questions/28885137/how-to-run-wget-inside-ubuntu-docker-image

FROM ubuntu:20.04
RUN  apt-get update \
  && apt-get install -y sed \
  && rm -rf /var/lib/apt/lists/*
COPY localize_tileset.sh localize_tileset.sh
RUN chmod a+x /localize_tileset.sh
ENTRYPOINT ["/localize_tileset.sh"]
