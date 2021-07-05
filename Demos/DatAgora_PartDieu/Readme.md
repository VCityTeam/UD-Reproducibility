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
