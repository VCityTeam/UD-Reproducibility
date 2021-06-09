FROM ubuntu:focal

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker/"

RUN apt-get update
ARG GEOSERVER_FQDN
ENV GEOSERVER_FQDN=${GEOSERVER_FQDN}
ARG GEOSERVER_PORT
ENV GEOSERVER_PORT=${GEOSERVER_PORT}
ARG TILESET_CUSTOM_SERVER
ENV TILESET_CUSTOM_SERVER=${TILESET_CUSTOM_SERVER}

######### Install the UD-Viz demo per se (client code) and build it
# Node version 14 is required. For its installation (on focal) refer to e.g.
#  https://computingforgeeks.com/install-node-js-14-on-ubuntu-debian-linux/
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y git


COPY SimpleServer /SimpleServer
COPY DatAgora_PartDieu /DatAgora_PartDieu
COPY img/ /DatAgora_PartDieu/assets/img/


RUN echo "{\n\"GEOSERVER_FQDN\": \"${GEOSERVER_FQDN}\" ,\n\"GEOSERVER_PORT\": \"${GEOSERVER_PORT}\" ,\n\"TILESET_CUSTOM_SERVER\": \"${TILESET_CUSTOM_SERVER}\" }" > data.json
RUN npm i -D nunjucks-cli
RUN node_modules/.bin/nunjucks config.njk data.json -p DatAgora_PartDieu/
RUN mv -b config.html config.json
RUN mv -f config.json DatAgora_PartDieu/assets/config/config.json


WORKDIR /DatAgora_PartDieu
RUN npm install
RUN npm run build

######## Install the ExpressJS server
WORKDIR /SimpleServer
RUN npm install
RUN npm run build

EXPOSE ${GEOSERVER_PORT}
CMD [ "node", "./index.js", "../DatAgora_PartDieu", "${GEOSERVER_PORT}" ]
