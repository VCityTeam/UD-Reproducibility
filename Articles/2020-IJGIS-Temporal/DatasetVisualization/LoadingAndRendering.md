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

* Install a 3DTiles web server: [3dtiles web server: DESKTOP developing context]() `../../../ExternalComponents/3DTilesSamples/Install3dTilesNodeBasedWebServer.md`

* Move the unzipped datasets you downloaded previously to
`3d-tiles-samples/tilesets/` and test that they are accessible by opening
the following URLs:
`http://localhost:8003/tilesets/Lyon_2009-2012-2015-3DTiles/Lyon_2009_Without_Remarkable_2_Tiles/tileset.json`
`http://localhost:8003/tilesets/Lyon_2009-2012-2015-3DTiles/Lyon_2012_Without_Remarkable_2_Tiles/tileset.json`
`http://localhost:8003/tilesets/Lyon_2009-2012-2015-3DTiles/Lyon_2015_Without_Remarkable_2_Tiles/tileset.json`
`http://localhost:8003/tilesets/Lyon_2009-2015_Without_Remarkable_2_Tiles/tileset.json`

##### Install specific to DS-3DTiles

* Intall the dedicated branch of the UD-Viz web client:

````
git clone https://github.com/MEPP-team/UDV.git
git checkout reproductibility/article-temporel-3DTiles
./install.sh
````

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

* The demo should be accessible at the following URL: http://localhost:8080/examples/ArticleTemporal/Demo.html.

* **Usage**:
  * Open the console to see the measured loading and rendering time
