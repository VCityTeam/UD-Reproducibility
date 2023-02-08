# How to compute Gratte Ciel Workspace

## Input data
https://partage.liris.cnrs.fr/index.php/s/j5mHkW8TZHtqF5b

## Generate Gratte Ciel Temporal Tilesets with Py3DTiles

## Transform Gratte Ciel Versions to RDF with UD-Graph
```
[UD-Graph Script]
./testTimestamp.sh
```
## Transform DifferencesAsGraph.JSON to RDF/OWL with CityGML model semantics
```
./diffToRDF.sh
./testMerge.sh
```