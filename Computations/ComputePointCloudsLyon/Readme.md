### Cloud Points- OpenData Lyon

To [visualize cloud points](http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/examples/DemoPC/Demo.html) from OpenData Lyon with UD-Viz :

* Download from the [open data website](https://data.beta.grandlyon.com/jeux-de-donnees/nuage-points-lidar-2015-metropole-lyon/donnees) and unzip it
  - wget "https://download.data.grandlyon.com/files/grandlyon/imagerie/mnt2015/lidar/1842_5172.zip" 
  - unzip 1842_5172.zip

* [Install LASzip](https://github.com/VCityTeam/UD-SV/blob/master/Tools/ToolForPointClouds.md#laszip) 
  and use lazip to uncompress the data (from laz to las) with e.g. `laszip -i 1842_5172/*.laz`

* Use [py3Dtiles](https://github.com/Oslandia/py3dtiles) to create 3DTiles from cloud points : 
  - `py3dtiles convert 1842_5172/*.las --out /dest`

* In the [generalDemoConfig.json](https://github.com/VCityTeam/UD-Viz/blob/master/UD-Viz-Core/examples/data/config/generalDemoConfig.json) :   
  * add the link to your dataset in a 3DTilesLayer
  * add a "pc_size" parameter to change the size of the point if needed. 

For information : Itowns can load colored cloud points natively

Note: the [generated data set](https://dataset-dl.liris.cnrs.fr/three-d-tiles-lyon-metropolis/2018/2018/Point_Cloud_Lyon_2018) is 3.9Gb, has ~44 000 files in the top level directory and 14 347 sub-directories... 


