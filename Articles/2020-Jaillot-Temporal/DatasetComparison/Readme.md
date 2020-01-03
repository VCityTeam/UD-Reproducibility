## Comparison of CityGML, 3D Tiles and 3D Tiles temporal datasets

We compared the following datasets:

### DS-CityGML

  * **Format**: CityGML
  * **Description**: composed of three independent snapshots of the buildings of
  the city of Lyon (2009, 2012 and 2015). They have been "stripped" from textures
  coordinates and images and from generic attributes that are not embedded in
  DS-3DTiles and DS-3DTilesTemporal (i.e. to make them comparable).
  * **Original data**: obtained from the [Grand Lyon open data website](https://data.beta.grandlyon.com/accueil)
  * **Final dataset download link**: TODO: Update avec les datasets downloaded
    patched et strippes car pour l'instant fait avec des remarkable dedans donc
    pas top et correspond pas à ceux qu'on visualise ensuite... (faire un seul
    depot zenodo qui contient trois .zip (un par vintage))
  * **How to reproduce the computation of this dataset**: TODO (cf todo ci dessus)

### DS-3DTiles

  * **Format**: 3D Tiles
  * **Description**: Conversion of DS-CityGML into the 3D Tiles format.
  * **Original data**: DS-CityGML
  * **Final dataset download link**: TODO (relancer le tiler sur DS-CityGML)
  * **How to reproduce the computation of this dataset**: TODO

### DS-3DTilesTmp

  * **Format**: 3D Tiles with temporal extension
  * **Description**: represents the buildings of Lyon between 2009 and 2015
  but stored as a time-evolving 3D city model in 3D Tiles with the temporal
  extension. It contains states of buildings with their time-spans and
  transactions between these states.
  * **Original data**: DS-CityGML
  * **Final dataset download link**: TODO (relancer le temporal tiler sur DS-CityGML)
  * **How to reproduce the computation of this dataset**: Reproduce the
  [ComputeLyon3DTilesTemporal](../../../Computations/ComputeLyon3DTilesTemporal)
  computation.

From these datasets we obtained the following comparison table:

|                |           | Size (MB) | **Number of buildings** |
|----------------|-----------|:---------:|:-----------------------:|
| DS-CityGML     | *2009*    |    1300   |          14827          |
|                | *2012*    |    1400   |          14835          |
|                | *2015*    |    976    |          24289          |
|                | **Total** |    3676   |        **53951**        |
| DS-3DTiles     | *2009*    |    202    |          14827          |
|                | *2012*    |    218    |          14835          |
|                | *2015*    |    319    |          24289          |
|                | **Total** |    739    |        **53951**        |
| DS-3DTiles-Tmp |           |    466    |        **36975**        |


*Notes on size computation*: Computed with `du -si` which gives the result in MB.
