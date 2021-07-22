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

## Running the demo for the first time
The only pre-requisite is to have a host with 
[docker compose](https://docs.docker.com/compose/) installed. Once docker is installed, start the docker daemon.

In order to launch the demo (from a terminal) clone this repository and
change the directory to be the one holding this Readme.md file and run the
following command (you can add "-d" at the end of this line to run the command in background):
```
docker-compose up
```

The setup building of images might take up to several minutes. Once the geoserver-setup docker exited, all the components should be up and running.
From this moment, you can:
 - access the web-gl based demo by browsing the `http://localhost:8999` URL
 - optionally access to the geoserver web interface by browsing the 
  `http://localhost:8998/geoserver` URL

By default, this demo uses ports between 8995 and 8999 included. These ports are configurable by editing the 
[docker-compose .env file](https://docs.docker.com/compose/env-file/)
located in the [same directory](.env). Refer to the comments within that file
for a documentation of the roles of the respective variables.

## Updating the demo

To ensure the update goes smoothly, you will need to run several commands to make sure docker won't use previously built images, thus preventing certain modules from updating.
(All the commands used in the tutorial below are documented [here](https://docs.docker.com/reference/))
First, you will need to stop the current demo. This can be done by going into the directory where this ReadMe is located, and run the following command :
```
docker-compose down
```
This will stop all the containers launched when you last ran the demo.

Next step is removing the outdated images. If you know which parts of the demo were updated precisely, you can use
```
docker images
```
to get the images id and then 
```
docker rmi <Image ID>
```
to remove each of the images. The names of the images built by this demo are written in the docker-compose.yml file


If you don't know exactly what to update,running the following command will remove all the images built by this demo that could have been updated, based on their name :
```
docker rmi -f $(sudo docker images "datagora*" -q)
```
If you have other datagora dockers with images prefixed with "datagora", you should refrain from using this method and remove the images one by one.

Once the images are removed, you will need to rebuild the demo. To ensure docker won't use cached data that may take priority over the new updated data, run the following command :
```
docker build --no-cache
```
Finally, when the build is completed, you can once again run (with "-d" if you need it in background.) :
```
docker compose up
```

## Setup

To setup this demo you can use the .env file available to configure several parameters for each of the six dockers used. To configure the UD-Viz view, you may need to configure the extent and camera settings directly in the config file. These parameters should be the same for each install of the demo and you won't need to change them for a standard install, but they can easily be modified if you need it.

If you need to reinstall the demo with different parameters, be sure to fully remove all the previous containers, images and volumes used by the previous demo to ensure no information remains cached.

## Known issues

### Dockers not awaiting each other

Some dockers need a docker to be up running so they can run and complete their task properly. In normal circumstances they do so. However, it has been observed on occasion that the SpatialMultimediaDB will start running while the postgres docker has not finished its setup, resulting in the SpatialMultimediaDB being unable to connect to the database.
If that occurs, relaunching the demo should solve the issue.

### Geoserver crashing when refreshing UD-Viz

We encountered an issue where reloading the UD-Viz webpage caused the geoserver to crash. This happened on a MAC while using Chrome browser.
It is not yet clear what caused this issue, but relaunching the demo ended up solving it.
