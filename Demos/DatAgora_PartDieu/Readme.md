## What this demo is about
A demo illustrating how to:
  - serve an [UD-Viz based](https://github.com/VCityTeam/UD-Viz) urban scene 
  - uploading several urban data files to 
    [geoserver](https://github.com/kartoza/docker-geoserver)
  - serving the corresponding urban data layers (with the same geoserver) for
    display in the urban scene  
  - additional display of building sets based on the 3DTiles format

This demo was developed for the 
[place of vegetation in cities project](https://github.com/VCityTeam/DatAgora/wiki/Vegetalization-Project)
within DatAgora.

## Temporary instructions (31/05/2021)
* Clone `https://github.com/VCityTeam/UD-Reproducibility` and switch to this branch `datagora_udviz_refacto`.
* Go to subdir `UD-Reproducibility/Demos/DatAgora_PartDieu`.
* Deploy and start containers : `docker-compose up`
* There is currently a bug with the UD-Viz container, to work around it, build and run UD-Viz manually:
  ```bash
  cd ud-viz-context/DatAgora_PartDieu/
  npm i
  npm run debug
  ```

## Running the demo
The only pre-requisite is to have a host with 
[docker compose](https://docs.docker.com/compose/) installed.

In order to launching the demo (from a terminal) clone this repository and
change the directory to be the one holding this Readme.md file and run the
following command :
```
docker-compose up
```

The setup building of images might take up to several minutes. Once the 
docker-compose is running the container, you can:
 - access the web-gl based demo by browsing the `http://localhost:8999` URL
 - optionally access to the geoserver web interface by browsing the 
  `http://localhost:8080/geoserver` URL
  
The above ports (the integer numbers present in the URL) are configurable by
editing the 
[docker-compose .env file](https://docs.docker.com/compose/env-file/)
present in the [same directory](.env). Refer to the comments within that file
for a documentation of the roles of the respective variables.
