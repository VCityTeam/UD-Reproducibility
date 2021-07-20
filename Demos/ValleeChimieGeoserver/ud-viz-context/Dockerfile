FROM ubuntu:focal

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker/"

RUN apt-get update
ARG GEOSERVER_FQDN
ENV GEOSERVER_FQDN=${GEOSERVER_FQDN}
ARG GEOSERVER_PORT
ENV GEOSERVER_PORT=${GEOSERVER_PORT}
ARG SPATIAL_MULTIMEDIA_DB_FQDN
ENV SPATIAL_MULTIMEDIA_DB_FQDN=${SPATIAL_MULTIMEDIA_DB_FQDN}
ARG SPATIAL_MULTIMEDIA_DB_PORT
ENV SPATIAL_MULTIMEDIA_DB_PORT=${SPATIAL_MULTIMEDIA_DB_PORT}
ARG TILESET_CUSTOM_SERVER
ENV TILESET_CUSTOM_SERVER=${TILESET_CUSTOM_SERVER}
ARG UD_VIZ_PORT
ENV UD_VIZ_PORT=${UD_VIZ_PORT}

######### Install the UD-Viz demo per se (client code) and build it
# Node version 14 is required. For its installation (on focal) refer to e.g.
#  https://computingforgeeks.com/install-node-js-14-on-ubuntu-debian-linux/
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y git

RUN git clone https://github.com/VCityTeam/UD-Viz-Template.git

WORKDIR /UD-Viz-Template
RUN git reset --hard 3cf254e5044542054be6d96be07f80c9e2a158d0

WORKDIR /
RUN cp -r UD-Viz-Template/DemoFull ValleeChimieGeoserver
RUN cp -r UD-Viz-Template/SimpleServer SimpleServer
RUN rm -fr UD-Viz-Template
COPY BaseDemo.js ValleeChimieGeoserver/src/Helpers/BaseDemo.js
COPY config.njk ValleeChimieGeoserver/config.njk

RUN echo "{\n\"GEOSERVER_FQDN\": \"${GEOSERVER_FQDN}\" ,\n\"GEOSERVER_PORT\": \"${GEOSERVER_PORT}\" ,\n\"TILESET_CUSTOM_SERVER\": \"${TILESET_CUSTOM_SERVER}\" ,\n\"SPATIAL_MULTIMEDIA_DB_FQDN\": \"${SPATIAL_MULTIMEDIA_DB_FQDN}\" ,\n\"SPATIAL_MULTIMEDIA_DB_PORT\": \"${SPATIAL_MULTIMEDIA_DB_PORT}\" }" > data.json
RUN npm i -D nunjucks-cli
RUN node_modules/.bin/nunjucks config.njk data.json -p ValleeChimieGeoserver/
RUN mv -b config.html config.json
RUN mv -f config.json ValleeChimieGeoserver/assets/config/config.json

WORKDIR /ValleeChimieGeoserver
RUN npm install
RUN npm run build

WORKDIR /SimpleServer
RUN npm install
RUN npm run build

EXPOSE ${UD_VIZ_PORT}
CMD [ "node", "./index.js", "../DatAgora_PartDieu", "--port=${UD_VIZ_PORT}" ]
