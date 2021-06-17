# 3DTiles Server

## General information

In the context of development (e.g. on your desktop)and if you need to handle over [3DTiles tilesets](https://github.com/AnalyticalGraphicsInc/3d-tiles) for your client to display then you can deploy a local (on your desktop computer) web (http) server. A quick and easy way to do so (on your desktop) consists in installing a (node.js based) [3d-tiles-samples](https://github.com/AnalyticalGraphicsInc/3d-tiles-samples) server.

## Simple to install 3DTiles web server ([node.js](https://nodejs.org/en/) based) 

### Manual installation
A quick manual installation goes
```
   git clone https://github.com/AnalyticalGraphicsInc/3d-tiles-samples
   cd 3d-tiles-samples
   npm install
   npm start
```
The tileset examples will then browsable at the `http://localhost:8003/tilesets/` 
address (since `8003` is the default port).

Run
```
   npm start -- help
```
for further server options e.g. `npm start -- --port 8080` will have the server
listen to the `8080` port

### Using docker
Use the [Dockerfile](Dockerfile) provided within the 3dtiles-server-context directory e.g. with
the commands
```
   docker build github.com/VCityTeam/UD-Reproducibility#master:ExternalComponents/3DTilesSamples \
                -t cesium-gs/3d-tiles-samples
   docker run cesium-gs/3d-tiles-samples
```

### Using docker-compose

 - Copy the context folder provided in this directory in your compose folder.
 - Create a .env file in your compose folder (if one already exists, do not create another)
 - Add the following code to your .env file :
 ```
 # The adress/directory where the tileset you want to upload to your server is located 
 TILESET_SOURCE=https://dataset-dl.liris.cnrs.fr/three-d-tiles-lyon-metropolis/Lyon_2015-gltf-repaired_TileSet/
 # The port used to access your server data (8996 by default)
 TILESET_SERVER_PORT=8996
 ```
 - Configure the variables to suit your needs.
 - Add the following code to your docker-compose.yml file as a service (if you need an example, see [this file](./Example/docker-compose.yml) for reference):
 ```
 3dtiles-server:
     build:
     context: ./3dtiles-server-context
     args:
         TILESET_SOURCE: ${TILESET_SOURCE}
         TILESET_SERVER_PORT: ${TILESET_SERVER_PORT}
     ports:
     - ${TILESET_SERVER_PORT}:${TILESET_SERVER_PORT}
 ```
 - Build and launch your docker-compose.
 - Your tileset should now be available at the following adress : localhost:<YOUR_SERVER_PORT>/tilesets/<YOUR_TILESET_NAME>
