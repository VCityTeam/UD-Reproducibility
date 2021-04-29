FROM ubuntu:focal

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker/"

RUN apt-get update

######### Install the UD-Viz demo per se (client code) and build it
# Node version 14 is required. For its installation (on focal) refer to e.g.
#  https://computingforgeeks.com/install-node-js-14-on-ubuntu-debian-linux/
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y git

COPY SimpleServer /SimpleServer
COPY DatAgora_PartDieu /DatAgora_PartDieu
COPY img/ /ChemistryValley/assets/img/
WORKDIR /DatAgora_PartDieu
RUN npm install
RUN npm run build

######### Install the ExpressJS server
WORKDIR /SimpleServer
RUN npm install
RUN npm run build

EXPOSE 80
CMD [ "node", "./index.js", "../DatAgora_PartDieu", "80" ]
