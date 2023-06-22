# How to compute Gratte Ciel Workspace

## Dependencies
- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Input data
The input data can be created from the [Gratte Ciel 3DTiles temporal tilset transformation workflow](../../3DTiles/GratteCielTemporal2009-2018/Readme.md) or can be found on [Nextcloud](https://partage.liris.cnrs.fr/index.php/s/j5mHkW8TZHtqF5b).

Store the CityGML files in a folder, that will be refered to as `[input folder]` in these instructions

## Setup
1. Install UD-Graph
```bash
git clone https://github.com/VCityTeam/UD-Graph.git
```
Copy the scripts in this directory folder to the following folders in the UD-Graph local repository
```bash
cp testGratteCiel.sh ./UD-Graph/Transformations/XML-to-RDF
cp testTimestamp.sh ./UD-Graph/Transformations/utilities
cp diffToRDF.sh ./UD-Graph/Transformations/DifferenceGraph-to-CityGML3
cp addMerge.sh ./UD-Graph/Transformations/utilities
```
## Step 1: Transform CityGML data to RDF
1. Edit the `[input folder]` entries in the [testGratteCiel.sh](./testGratteCiel.sh) script to match the path where the input data is stored.
2. Execute transformation XML to RDF
```bash
cd UD-Graph/Transformations/XML-to-RDF
./testGratteCiel.sh
``` 

## Step 2: Transform Gratte Ciel Versions to RDF
1. Add timestamps to the transformed CityGML data
```bash
cd ../utilities
./testTimestamp.sh
```

## Transform DifferencesAsGraph.JSON to RDF/OWL with CityGML semantics
```bash
cd ../DifferenceGraph-to-CityGML3
./diffToRDF.sh
cd ../utilities
./testMerge.sh
```