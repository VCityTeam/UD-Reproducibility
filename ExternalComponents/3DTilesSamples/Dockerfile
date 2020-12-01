FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN apt-get install -y git

RUN git clone https://github.com/AnalyticalGraphicsInc/3d-tiles-samples
WORKDIR /3d-tiles-samples/
RUN npm install
EXPOSE 8003
# The "--public" flag informs the server to also listen to all interfaces
# which includes listening to requests coming "from" the container. Refer
# to the command line documentation obtained by running `npm start -- help`
# (as opposed to running `npm start -- --help`).
CMD [ "npm", "start", "--", "--public" ]

