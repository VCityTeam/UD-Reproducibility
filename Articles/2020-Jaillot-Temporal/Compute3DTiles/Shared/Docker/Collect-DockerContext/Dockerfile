FROM ubuntu:18.04
LABEL vendor="UD-SV project"

# Core dependencies
# rm, mkdir, mv
RUN apt-get update
RUN apt-get -y install sed
RUN apt-get -y install wget
RUN apt-get -y install unzip
RUN apt-get -y install patch

COPY ./collect_data.sh /
COPY ./DataPatches /DataPatches/
RUN chmod a+x /collect_data.sh
ENTRYPOINT ["/collect_data.sh"]
#CMD []
