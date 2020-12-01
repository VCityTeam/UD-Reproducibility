## Simple to install 3DTiles web server ([node.js](https://nodejs.org/en/) based) 

In the context of development (e.g. on your desktop)and if you need to handle over [3DTiles tilesets](https://github.com/AnalyticalGraphicsInc/3d-tiles) for your client to display then you can deploy a local (on your desktop computer) web (http) server. A quick and easy way to do so (on your desktop) consists in installing a (node.js based) [3d-tiles-samples](https://github.com/AnalyticalGraphicsInc/3d-tiles-samples) server.

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
for further server options e.g. `npm start -- -port 8080` will have the server
listen to the `8080` port

### Using docker
Use the [Dockerfile](Dockerfile) provided within this directory e.g. with
the commands
```
   docker build github.com/VCityTeam/UD-Reproducibility#master:ExternalComponents/3DTilesSamples cesium-gs/3d-tiles-samples
   docker run cesium-gs/3d-tiles-samples
```


