FROM node:latest

LABEL maintainer "VCityTeam"

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y wget

ARG TILESET_SOURCE
ENV TILESET_SOURCE=${TILESET_SOURCE}

RUN git clone https://github.com/AnalyticalGraphicsInc/3d-tiles-samples

# Import an example of 3DTiles embedding some IFC geometry
WORKDIR /3d-tiles-samples/tilesets/

RUN wget --recursive --no-parent --no-host-directories --cut-dirs=1 -R 'index.html?*' ${TILESET_SOURCE}


WORKDIR /3d-tiles-samples/
RUN npm install
EXPOSE 8003
CMD [ "npm", "start", "--", "--public" ]