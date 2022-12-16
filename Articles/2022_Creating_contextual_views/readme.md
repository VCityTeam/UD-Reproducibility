### To reproduce the full demonstration 

## Create the 3DTiles dataset from the ifc file :

- Download [this ifc file](https://github.com/VCityTeam/UD-Sample-data/blob/master/Ifc/Chaufferie_doua.ifc)

- Install the [Py3DTilers Docker](https://github.com/VCityTeam/py3dtilers-docker)
- Run the following command line to create the 3DTiles tileset :
  - docker run --rm -t vcity/py3dtilers ifc-tiler --ifc_path PATH_TO_YOUR_FILE --offset 0 0 0 -170

## Set up an http server to serve the created 3DTiles 

- Use this [3DTiles-Server docker](https://github.com/VCityTeam/3DTiles-Server-docker)
  -  `docker build 3dtiles-server-context -t 3dtiles-server --build-arg TILESET_SOURCE=<Your_Tileset_Source>`
  -  `docker run 3dtiles-server`

## Install BimServer to retrieve semantic data from the create 3DTiles tileset

- Install BIM Server using [this docker](https://github.com/VCityTeam/Bimserver-docker)

## Install and run the UD-Viz demonstration 
- Install the [UD-Viz Ifc demonstration](https://github.com/VCityTeam/UD-Demo-Vcity-IFC)   
  - Follow [this part](https://github.com/VCityTeam/UD-Demo-Vcity-IFC#to-get-semantic-data-from-the-ifc-file) of the installation to use the bimserver correctly

- Run the demonstration
