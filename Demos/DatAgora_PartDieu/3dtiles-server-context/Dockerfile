FROM node:latest

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker/"

RUN apt-get update
RUN apt-get install -y git
RUN apt-get install -y wget

ARG TILESET_SOURCE
ENV TILESET_SOURCE = ${TILESET_SOURCE}

RUN git clone https://github.com/AnalyticalGraphicsInc/3d-tiles-samples

# Import an example of 3DTiles embedding some IFC geometry
WORKDIR /3d-tiles-samples/tilesets/

RUN wget --recursive --no-parent -nH --cut-dirs=1 --reject="index.html*" \
    https://dataset-dl.liris.cnrs.fr/three-d-tiles-lyon-metropolis/Lyon_2015-gltf-repaired_TileSet/

WORKDIR /3d-tiles-samples/
RUN npm install
EXPOSE 8003
# CMD [ "npm", "start", "--", "--host=0.0.0.0", "--port=8996" ]
CMD [ "npm", "start", "--", "--public" ]