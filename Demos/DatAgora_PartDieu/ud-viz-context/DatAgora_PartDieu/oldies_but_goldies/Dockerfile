FROM ubuntu:focal

LABEL maintainer "VCityTeam"
LABEL source.repo "https://github.com/VCityTeam/UD-Viz-docker/"

RUN apt-get update

######### Install UD-Viz and build it with npm
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN apt-get install -y git

RUN mkdir -p WebDemos
WORKDIR /WebDemos
RUN git clone https://github.com/VCityTeam/UD-Viz.git
WORKDIR /WebDemos/UD-Viz/UD-Viz-Core
COPY DemoConfigData.json examples/DemoFull/DemoConfigData.json
COPY index.html ./index.html
COPY Demo.js examples/DemoFull/Demo.js
COPY Demo.html examples/DemoFull/Demo.html
COPY img examples/DemoFull/img

RUN npm install
RUN npm run build 

EXPOSE 8999

CMD ["npm","start","--","--host=0.0.0.0","--port=8999"] 

