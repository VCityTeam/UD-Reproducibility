### Cloud Points - OpenData Lyon

To [visualize cloud points](https://point-cloud.vcityliris.data.alpha.grandlyon.com/) from OpenData Lyon with UD-Viz :

* Download from the [open data website](https://data.beta.grandlyon.com/jeux-de-donnees/nuage-points-lidar-2015-metropole-lyon/donnees) and unzip it
  - wget "https://download.data.grandlyon.com/files/grandlyon/imagerie/mnt2015/lidar/1842_5172.zip" 
  - unzip 1842_5172.zip

* [Install LASzip](https://github.com/VCityTeam/UD-SV/blob/master/Tools/ToolForPointClouds.md#laszip) 
  and use lazip to uncompress the data (from laz to las) with e.g. `laszip -i 1842_5172/*.laz`

* Use [py3Dtiles](https://github.com/Oslandia/py3dtiles) to create 3DTiles from cloud points : 
  - `py3dtiles convert 1842_5172/*.las --out /dest`




