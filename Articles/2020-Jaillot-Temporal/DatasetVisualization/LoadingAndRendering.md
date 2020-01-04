## Time for loading and rendering DS-3DTiles and DS-3DTiles-Tmp

### The results

The following table presents the mean time and standard deviation for loading
and rendering DS-3DTiles and DS-3DTiles-Tmp, measured on 10 samples:

|                    |           | **Mean loading and rendering time (seconds)** | **Standard deviation (seconds)**  |
|--------------------|-----------|:---------------------------------------------:|:---------------------------------:|
| **DS-3DTiles**     | *2009*    |                      1.4                      |                0.03               |
|                    | *2012*    |                      1.4                      |                0.04               |
|                    | *2015*    |                      1.9                      |                0.1                |
|                    | **Total** |                    **4.7**                    |                N.A.               |
| **DS-3DTiles-Tmp** |           |                     **3**                     |                0.04               |

### Reproduce these results

* Download [DS-3DTiles](../DatasetComparison/Readme.md#DS-3DTiles) and
[DS-3DTiles-Tmp](../DatasetComparison/Readme.md#DS-3DTiles-Tmp).

* Unzip these datasets

* Install a 3DTiles web server: [3dtiles web server: DESKTOP developing context](../../../ExternalComponents/3DTilesSamples/Install3dTilesNodeBasedWebServer.md)

* Move the unzipped datasets you downloaded previously to
`3d-tiles-samples/tilesets/` and test that they are accessible by opening
the following URLs:
TODO: change this URL by the correct URLS
`http://localhost:8003/tilesets/Lyon_2009-2015_Without_Remarkable_32_Tiles/tileset.json`

##### Install specific to DS-3DTiles

* Intall the dedicated branch of the UD-Viz web client:

````
git clone https://github.com/MEPP-team/UDV.git
git checkout reproductibility/article-temporel-3DTiles
./install.sh
````
* Replace the URLs of the [3D Tiles layers config in the UD-Viz configuration file](https://github.com/VCityTeam/UD-Viz/blob/reproductibility/article-temporel-3DTiles/UDV-Core/examples/data/config/generalDemoConfig.json#L43) by the URLS of the vintages
of DS-3DTiles; i.e. replace the:
  * `building-lyon-2009`, `building-lyon-2012` and `building-lyon-2015` URLS by:
TODO: either give the correct URLS or replace this step and commit the correct URLS

* Run UD-Viz: `npm start`

* The demo should be accessible at the following URL: http://localhost:8080/examples/DemoArticle/Demo.html.

* **Usage**:
  * Choose the vintage to display (Lyon in 2009, 2012 or 2015) by commenting /
  uncommenting one of the following three lines in `examples/DemoArticle/Demo.js`:

```
baseDemo.add3DTilesLayer('building-lyon-2009');
// baseDemo.add3DTilesLayer('building-lyon-2012');
// baseDemo.add3DTilesLayer('building-lyon-2015');
```
  * Open the console to see the measured loading and rendering times

#### Install specific to DS-3DTiles-Tmp

* Intall the dedicated branch of the UD-Viz web client:

````
git clone https://github.com/MEPP-team/UDV.git
git checkout article-temporel-3DTilesTemporal
./install.sh
````
* Replace the URL of the [3D Tiles Temporal layer config in the UD-Viz configuration file](https://github.com/VCityTeam/UD-Viz/blob/reproductibility/article-temporel-3DTilesTemporal/UDV-Core/examples/data/config/generalDemoConfig.json#L18) by the URL of the
of DS-3DTiles-Tmp dataset.
TODO: update the "SmallTiles" and "BigTiles" to leave only one and put the right
URL directly in it. Then, remove this item.

* The demo should be accessible at the following URL: http://localhost:8080/examples/ArticleTemporal/Demo.html.

* **Usage**:
  * Open the console to see the measured loading and rendering time
