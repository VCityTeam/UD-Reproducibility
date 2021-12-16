### Cloud Points - OpenData Lyon

To [visualize cloud points](https://point-cloud.vcityliris.data.alpha.grandlyon.com/) from OpenData Lyon with UD-Viz :

* Download from the [open data website](https://data.beta.grandlyon.com/jeux-de-donnees/nuage-points-lidar-2015-metropole-lyon/donnees) and unzip it
  - wget "https://download.data.grandlyon.com/files/grandlyon/imagerie/mnt2015/lidar/1842_5172.zip" 
  - unzip 1842_5172.zip

* [Install LASzip](https://github.com/VCityTeam/UD-SV/blob/master/Tools/ToolForPointClouds.md#laszip) 
  and use lazip to uncompress the data (from laz to las) with e.g. `laszip -i 1842_5172/*.laz`

* Use [py3Dtiles](https://github.com/Oslandia/py3dtiles) to create 3DTiles from cloud points : 
  - `py3dtiles convert 1842_5172/*.las --out /dest`

Note: the [generated data set](https://dataset-dl.liris.cnrs.fr/three-d-tiles-lyon-metropolis/2018/2018/Point_Cloud_Lyon_2018) is 3.9Gb, has ~44 000 files in the top level directory and 14 347 sub-directories... 


