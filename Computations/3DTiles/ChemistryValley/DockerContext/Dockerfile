FROM ubuntu:focal

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Reproducibility/"

RUN apt-get update

### Command dependencies
RUN apt-get install -y git
RUN apt-get install -y curl

ARG POSTGRES_HOST
ENV PG_HOST=$POSTGRES_HOST
ARG POSTGRES_PORT
ENV PG_PORT=$POSTGRES_PORT
ARG POSTGRES_DB
ENV PG_NAME=$POSTGRES_DB
ARG POSTGRES_USER
ENV PG_USER=$POSTGRES_USER
ARG POSTGRES_PASSWORD
ENV PG_PASSWORD=$POSTGRES_PASSWORD

# The installation of add-apt-repository depends itself on tzdata that requires
# some interactive configuration. The following is a non interactive workaround,
# refer to
# https://stackoverflow.com/questions/8671308/non-interactive-method-for-dpkg-reconfigure-tzdata/20693661
ARG DEBIAN_FRONTEND=noninteractive
ARG DEBCONF_NONINTERACTIVE_SEEN=true
RUN echo "tzdata tzdata/Areas select Europe" > preseed.txt
RUN echo "tzdata tzdata/Zones/Europe select Berlin" >> preseed.txt
RUN debconf-set-selections preseed.txt
# Why running in sequence and update and the install ? Read the small prints of 
# https://stackoverflow.com/questions/32486779/apt-add-repository-command-not-found-error-in-dockerfile
RUN apt update && apt install -y software-properties-common

RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt-get install -y python3.7
# Installing pip with
#    RUN apt-get install -y python3-pip
# seems to fail. We thus follow
# https://stackoverflow.com/questions/52677089/how-to-install-pip-for-python3-7-only
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.7 get-pip.py
# Done with python3.7 install

# Only the docker client refer to e.g.
# https://stackoverflow.com/questions/38675925/is-it-possible-to-install-only-the-docker-cli-and-not-the-daemon
ENV DOCKERVERSION=18.03.1-ce
RUN curl -fsSLO https://download.docker.com/linux/static/stable/x86_64/docker-${DOCKERVERSION}.tgz \
  && tar xzvf docker-${DOCKERVERSION}.tgz --strip 1 \
                 -C /usr/local/bin docker/docker \
  && rm docker-${DOCKERVERSION}.tgz

###
RUN git clone https://github.com/VCityTeam/UD-Reproducibility
WORKDIR UD-Reproducibility
RUN git reset --hard cc0a83da1e7e7fab5a0d80e9b8450aa7493f6663
WORKDIR Computations/3DTiles/LyonTemporal/PythonCallingDocker
RUN pip3 install -r requirements.txt

WORKDIR DemoStatic

SHELL ["/bin/bash", "-c"]
RUN printf "output_dir = 'junk' \n\
vintage = 2015\n\
city = 'CHEMISTRY_VALLEY'\n\
boroughs = [\n\
           'LYON_1ER',\n\
]\n\
 \n\
database = {\n\
  'PG_HOST': '${PG_HOST}',\n\
  'PG_PORT': '${PG_PORT}',\n\
  'PG_NAME': '${PG_DB}',\n\
  'PG_USER': '${PG_USER}',\n\
  'PG_PASSWORD': '${PG_PASSWORD}'\n\
}" > demo_configuration_static.py

COPY entrypoint.sh entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"] 