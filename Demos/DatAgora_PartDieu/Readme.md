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

## Running the demo
The only pre-requisite is to have a host with 
[docker compose](https://docs.docker.com/compose/) installed.

You first need to configure three things:
 - Edit the [`.env`](.env) file to suit your needs (e.g. change the
   services port numbers)
 - within the `ud-viz-context/DemoConfigData.json` file adapt the 
   `localhost:8999` string of the `geoserver` entry to become 
   the fully qualified domain name of the server that will host
   the demo together with the port number that you configured in 
   the `.env`. This `geoserver` entry should be of the form
   ```
   geoserver":"http://<fully-qualified-domain-name-of-server>:<chosen-port>/geoserver/cite/ows?",
   ```
   Note that the geoserver hostname and the port number should match the
   choices you made in the `.env` file.
 - within the `docker-compose.yml` file, and within the `udviz` service
   section, edit the command in order to provide the IP address of the host
   ```
   command : npm start -- --host=<host-IP-address> --port=${UD_VIZ_PORT} 
   ```

In order to launch the demo (from a terminal) clone this repository and
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
