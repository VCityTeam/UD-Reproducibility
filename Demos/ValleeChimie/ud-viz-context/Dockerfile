FROM ubuntu:focal

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker/"

RUN apt-get update

# The container will serve (through http) both:
#  1. the client code
#  2. the data required by the demo
# Both (client and data) will be served by a single Appache2 http server
# configured to expose (refer to Apache2's DocumentRoot variable) the
# DOCUMENT_ROOT sub-directory.

######### Expose (through http) the 3DTiles tilesets
# The tilesets are required by the demo.
# References concerning the wget ad-hoc flags
# https://askubuntu.com/questions/719410/wget-web-crawler-retrieves-unwanted-index-html-index-files
RUN mkdir -p /ChemistryValley/DataStore
WORKDIR /ChemistryValley/DataStore
RUN apt-get install -y wget
RUN wget --recursive --no-parent --no-host-directories --cut-dirs=1 -R 'index.html?*' https://dataset-dl.liris.cnrs.fr/three-d-tiles-lyon-metropolis/Chemistry-Valley_2015_TileSet/

######### Install the UD-Viz demo per se (client code) and build it
# Node version 14 is required. For its installation (on focal) refer to e.g.
#  https://computingforgeeks.com/install-node-js-14-on-ubuntu-debian-linux/
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs
RUN apt-get install -y git

COPY SimpleServer /SimpleServer
COPY ChemistryValley /ChemistryValley
COPY img/ /ChemistryValley/assets/img/
WORKDIR /ChemistryValley
RUN npm install
RUN npm run build

######### Install the ExpressJS server
WORKDIR /SimpleServer
RUN npm install
RUN npm run build

EXPOSE 80
CMD [ "node", "./index.js", "../ChemistryValley", "80" ]
