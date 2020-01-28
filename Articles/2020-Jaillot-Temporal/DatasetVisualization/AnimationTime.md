## Animation time (i.e. temporal navigation) comparison

### The results

The following figures compare the animation time for temporal navigation in
DS-3DTiles and DS-3DTiles-Tmp:

<figure>
  <img src="Images/animation-time.png" alt="drawing" width="350"/>
  <figcaption>Figure 1 - Animation time comparison of DS-3DTiles (3D Tiles) and
  DS-3DTiles-Tmp (3D tiles with temporal extension).</figcaption>
</figure>

<br/><br/>

<figure>
  <img src="Images/temporal-navigation.png" alt="drawing" width="600"/>
  <figcaption>Figure 2 - Temporal navigation comparison between 3D Tiles and 3D Tiles with temporal extension.</figcaption>
</figure>

<br/><br/>

**Succinct description of the figures (more details can be found in the paper):**

Figure 1 presents a comparison of the animation time when navigating between timestamps with DS-3DTiles (3D Tiles) and DS-3DTiles-Tmp (3D Tiles temporal extension). Each box represents a state at a given date indicated inside the box. The arrows express a change of state. The mean loading and rendering time (seconds) are respectively in black for DS-3DTiles and in green for DS-3DTiles-Tmp (indicated as xx seconds / xx seconds).

Figure 2 presents the navigation time between two timestamps.

### Reproduce these results

* All the values indicated on these images (excepted the 0.1 of DS-3DTiles-Tmp for temporal navigation) are deduced from [this result](LoadingAndRendering.md). They can be reproduced by following the notes to reproduce it.

* To obtain the 0.1 value corresponding to the temporal navigation in DS-3DTiles-Tmp, you can also use the [above-mentioned reproducibility notes](LoadingAndRendering.md). However, to obtain this value, you must open the temporal module from the left side menu bar. Then, switch the time with the time slider. The measured time is logged in the console of your web browser.

#### Temporal navigation in DS-3DTiles-Tmp evaluation

* Download [DS-3DTiles-Tmp](../DatasetComparison/Readme.md#DS-3DTiles-Tmp).

* Unzip this dataset

* Install a 3DTiles web server: [3dtiles web server: DESKTOP developing context](../../../ExternalComponents/3DTilesSamples/Install3dTilesNodeBasedWebServer.md)

* Move the unzipped dataset you downloaded previously to `3d-tiles-samples/tilesets/` and test that it are accessible by opening the following URL:
`http://localhost:8003/tilesets/Lyon_2009-2015_Without_Remarkable_2_Tiles/tileset.json`

* Install the dedicated branch of the UD-Viz web client:

````
git clone https://github.com/MEPP-team/UDV.git
git checkout article-temporel-3DTilesTemporal
./install.sh
````

* The demo should be accessible at the following URL: http://localhost:8080/examples/ArticleTemporal/Demo.html.

* **Usage**:
  * You can find the available modules of the demo in the sidebar situated on the
left side of the web page. Among these modules, the `Temporal Navigation` module
allows to navigate in time. Clicking on it opens a time slider at the bottom of
the page which you can use to change the display date.

  * Open the console to see the measured time for switching the display when changing the display date.
