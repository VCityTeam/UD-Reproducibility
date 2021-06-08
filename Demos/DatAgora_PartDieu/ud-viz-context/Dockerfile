FROM ubuntu:focal

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker/"

RUN apt-get update
ARG GEOSERVER_FQDN
ENV GEOSERVER_FQDN=${GEOSERVER_FQDN}
ARG GEOSERVER_PORT
ENV GEOSERVER_PORT=${GEOSERVER_PORT}

######### Install the UD-Viz demo per se (client code) and build it
# Node version 14 is required. For its installation (on focal) refer to e.g.
#  https://computingforgeeks.com/install-node-js-14-on-ubuntu-debian-linux/
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y git
RUN echo `GEOSERVER_FQDN: ` ${GEOSERVER_FQDN} `,` > input.json
RUN echo `GEOSERVER_PORT: ` ${GEOSERVER_PORT}    >> input.json
COPY SimpleServer /SimpleServer
COPY DatAgora_PartDieu /DatAgora_PartDieu
RUN npm i -D nunjucks-cli

RUN node_modules/.bin/nunjucks DatAgora_PartDieu/assets/config/config.tpl input.json
RUN mv config.hmtl DatAgora_PartDieu/assets/config/config.json

COPY img/ /DatAgora_PartDieu/assets/img/
WORKDIR /DatAgora_PartDieu
RUN npm install
RUN npm run build

######## Install the ExpressJS server
WORKDIR /SimpleServer
RUN npm install
RUN npm run build

EXPOSE 8999
CMD [ "node", "./index.js", "../DatAgora_PartDieu", "8999" ]
