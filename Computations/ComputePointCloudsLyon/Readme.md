### Cloud Points- OpenData Lyon

To [visualize cloud points](http://rict2.liris.cnrs.fr/UD-Viz/UD-Viz-Core/examples/DemoPC/Demo.html) from OpenData Lyon with UD-Viz :

* Download from the [open data website](https://data.beta.grandlyon.com/jeux-de-donnees/nuage-points-lidar-2015-metropole-lyon/donnees) and unzip it
  -     wget "https://download.data.grandlyon.com/files/grandlyon/imagerie/mnt2015/lidar/1842_5172.zip" 
  -     unzip 1842_5172.zip

* Install LASzip
  - On [Un*x](https://laszip.org/)
  - on OSX
    1. the short way with [LASTools](https://lastools.github.io/):
       ```bash
       wget https://lastools.github.io/download/LAStools.zip
       unzip LAStools.zip
       cd LAStools
       make                               # Reported to work with clang version 11.0.0 on OSX 10.4.6 (Mojave)
       cp bin/laszip /usr/local/bin       # For example
       ```
    2. the longer way with [pdal](http://pdal.io/): `brew install pdal`
  
* Use lazip to uncompress the data (from laz to las) with e.g. `laszip -i 1842_5172/*.laz`

* Use [py3Dtiles](https://github.com/Oslandia/py3dtiles) to create 3DTiles from cloud points : 
  - `py3dtiles convert 1842_5172/*.las --out /dest`

* In the [generalDemoConfig.json](https://github.com/VCityTeam/UD-Viz/blob/master/UD-Viz-Core/examples/data/config/generalDemoConfig.json) :   
  * add the link to your dataset in a 3DTilesLayer
  * add a "pc_size" parameter to change the size of the point if needed. 

For information : Itowns can load colored cloud points natively


