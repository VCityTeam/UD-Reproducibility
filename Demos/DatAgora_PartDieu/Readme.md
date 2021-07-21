## What this demo is about
A demo illustrating how to:
  - serve an [UD-Viz based](https://github.com/VCityTeam/UD-Viz) urban scene, that includes [SpatialMultimediaDB content display](https://github.com/VCityTeam/UD-Serv/tree/master/API_Enhanced_City)
  - uploading several urban data files to 
    [geoserver](https://github.com/kartoza/docker-geoserver)
  - serving the corresponding urban data layers (with the same geoserver) for
    display in the urban scene  
  - additional display of building sets based on the 3DTiles format

This demo was developed for the 
[place of vegetation in cities project](https://github.com/VCityTeam/DatAgora/wiki/Vegetalization-Project)
within DatAgora.

The dockers used in this demo are either located in this folder or in the [Docker folder](../../Docker) located in this repository.

## Running the demo
The only pre-requisite is to have a host with 
[docker compose](https://docs.docker.com/compose/) installed. Once docker is installed, start the docker daemon.

In order to launch the demo (from a terminal) clone this repository and
change the directory to be the one holding this Readme.md file and run the
following command :
```
docker-compose up
```

The setup building of images might take up to several minutes. Once the 
docker-compose is running the containers, you can:
 - access the web-gl based demo by browsing the `http://localhost:8999` URL
 - optionally access to the geoserver web interface by browsing the 
  `http://localhost:8998/geoserver` URL

By default, this demo uses ports between 8995 and 8999 included. These ports are configurable by editing the 
[docker-compose .env file](https://docs.docker.com/compose/env-file/)
located in the [same directory](.env). Refer to the comments within that file
for a documentation of the roles of the respective variables.


## Setup

To setup this demo you can use the .env file available to configure several parameters for each of the six dockers used. To configure the UD-Viz view, you may need to configure the extent and camera settings directly in the config file. These parameters should be the same for each install of the demo and you won't need to change them for a standard install, but they can easily be modified if you need it.

If you need to reinstall the demo with different parameters, be sure to fully remove all the previous containers, images and volumes used by the previous demo to ensure no information remains cached.
