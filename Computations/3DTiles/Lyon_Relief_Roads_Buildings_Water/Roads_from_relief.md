# Place roads with relief

This document explains how to use the 3DTiles models of the relief and the bridges to update the roads data with the correct altitudes.

We use the [Roads-from-relief](https://github.com/LorenzoMarnat/Roads-From-Relief) application to update the altitudes of the roads.

## Roads data

The roads data is taken from [IGN's BDTopo](https://geoservices.ign.fr/ressource/161992) open data. The roads are contained in _BDTOPO/1\_DONNEES\_LIVRAISON/BDT/TRANSPORT/TRONCON\_DE\_ROUTE.shp_.

On the [IGN's documentation](https://geoservices.ign.fr/sites/default/files/2021-11/DC_BDTOPO_3-0_1.pdf), we can see that the roads have an attribute called `POS_SOL`.
This attribute tells if the road is under the ground (`POS_SOL` <= -1), on the ground (`POS_SOL` = 0) or above the ground (`POS_SOL` >= 1).  
![image](https://user-images.githubusercontent.com/32875283/143593984-ce7913f5-4fcb-4d9a-8ad0-7c4ad065cc90.png)

To be able to place the roads correctly, we have to split the roads in 3 different files (`POS_SOL` <= -1, `POS_SOL` = 0 and `POS_SOL` >= 1). We use QGIS to do so:  
![image](https://user-images.githubusercontent.com/32875283/143594375-d1b0e72c-63dd-44bf-bf04-4fa6d9f55788.png)

The data must be saved as __GeoJSON__ with the EPSG 3946 projection.  
![image](https://user-images.githubusercontent.com/32875283/143594827-f8b4d8c5-5912-49b8-8059-c388544a9260.png)

![image](https://user-images.githubusercontent.com/32875283/143594840-d90fdcb4-1165-4b29-b367-d2d168a51aba.png)

## Update the altitudes

To update the altitudes of the roads, first [install and launch the Roads-from-relief](https://github.com/LorenzoMarnat/Roads-From-Relief#installation) application.

Then, you can update a file by drag-and-dropping it on the browser. The altitudes will be updated by raycasting on __all visible 3DTiles layers__.
If you don't want to use the relief or the bridges to update your file, hide the corresponding layer.
Once the update is over, a new file containing the roads with the right altitudes will be downloaded.

On the 3 files created before, only 2 need to be updated: the one containing the roads with `POS_SOL` <= -1 can be used __without update__.

To place the roads on the ground (`POS_SOL` = 0), __hide the bridges__. A file called _new\_..._ will be downloaded once the computation is over.  
![image](https://user-images.githubusercontent.com/32875283/143596289-c4e25abc-e9e5-40e2-9ceb-782d358fdfc1.png)

To place the roads above the ground (`POS_SOL` >= 1), __use both relief and bridges__.  
![image](https://user-images.githubusercontent.com/32875283/143597282-f44661a5-1c44-4619-99fc-fec87659bfe8.png)

## Create the 3DTiles roads

Put the 3 files (`POS_SOL` <= -1 and the 2 updated files) in a folder. This folder __must not contain__ any other .json or .geojson files.  

Use the [GeojsonTiler](https://github.com/VCityTeam/py3dtilers/tree/master/py3dtilers/GeojsonTiler)
(see the [installation notes](https://github.com/VCityTeam/py3dtilers#installation-from-sources) to install the Tiler) to create the 3DTiles from the GeoJSON files.

To run the GeojsonTiler, use:

```bash
geojson-tiler --path path/to/roads_folder/ --height 0.5
```

It will create a 3DTiles tileset from all the GeoJSON files contained in _roads_folder_. The 3D roads will have a height of 0.5 meter.
