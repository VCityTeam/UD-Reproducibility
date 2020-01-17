## Comparison of CityGML, 3D Tiles and 3D Tiles temporal datasets

### DS-CityGML

  * **Format**: CityGML
  * **Description**: composed of three independent snapshots of the buildings of
  the city of Lyon (2009, 2012 and 2015). They have been "stripped" from textures
  coordinates and images and from generic attributes that are not embedded in
  DS-3DTiles and DS-3DTilesTemporal (i.e. to make them comparable).
  * **Original data**: obtained from the [Grand Lyon open data website](https://data.beta.grandlyon.com/accueil)
  * **Final dataset download link**: https://doi.org/10.5281/zenodo.3611354
  * **How to reproduce the computation of this dataset**: Reproduce the
  [ComputeLyon3DTilesTemporal](../../../Computations/ComputeLyon3DTilesTemporal)
  computation. In the output directory, DS-CityGML is the composition of the `Lyon_2009_Splitted_Stripped`, `Lyon_2012_Splitted_Stripped` and `Lyon_2015_Splitted_Stripped` folders.

### DS-3DTiles

  * **Format**: 3D Tiles
  * **Description**: Conversion of DS-CityGML into the 3D Tiles format.
  * **Original data**: DS-CityGML
  * **Final dataset download link**: https://doi.org/10.5281/zenodo.3611357
  * **How to reproduce the computation of this dataset**: Reproduce the following computations:
    * [2009 vintage computation](../../../Computations/ComputeLyon3DTiles2009)
    * [2012 vintage computation](../../../Computations/ComputeLyon3DTiles2012)
    * [2015 vintage computation](../../../Computations/ComputeLyon3DTiles2015)
    
### DS-3DTiles-Tmp

  * **Format**: 3D Tiles with temporal extension
  * **Description**: represents the buildings of Lyon between 2009 and 2015
  but stored as a time-evolving 3D city model in 3D Tiles with the temporal
  extension. It contains states of buildings with their time-spans and
  transactions between these states.
  * **Original data**: DS-CityGML
  * **Final dataset download link**: https://doi.org/10.5281/zenodo.3611403
  * **How to reproduce the computation of this dataset**: Reproduce the
  [ComputeLyon3DTilesTemporal](../../../Computations/ComputeLyon3DTilesTemporal)
  computation. DS-3DTiles-Tmp is in the `Result` folder once the computation is finished.

### Resulting comparison

From these datasets we obtained the following comparison table:

|                |           | Size (MB) | **Number of buildings** |
|----------------|-----------|:---------:|:-----------------------:|
| **DS-CityGML** | *2009*    |    1100   |          14827          |
|                | *2012*    |    1100   |          14835          |
|                | *2015*    |    976    |          24289          |
|                | **Total** |  **3176** |        **53951**        |
| **DS-3DTiles** | *2009*    |    202    |          14827          |
|                | *2012*    |    218    |          14835          |
|                | *2015*    |    319    |          24289          |
|                | **Total** |  **739**  |        **53951**        |
|**DS-3DTiles-Tmp**|           |  **466**  |        **36975**        |


**Note**: The size has been computed with `du --si` which gives the result in MB.
