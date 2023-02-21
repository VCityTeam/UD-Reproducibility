# Temporal Tileset for Gratte Ciel
This is a manual calculation of a 3DTiles+temporal extention of a small data set of the Gratte Ciel neighborhood with 2 scenarios of evolutuion.

![gratte-ciel-workspace illustration](./gratte-ciel-workspace.svg)

The input and the output data for each stage - as calculated thus - far can be found on [nextcloud](https://partage.liris.cnrs.fr/index.php/f/151016)
The final dataset is online and available [here](https://dataset-dl.liris.cnrs.fr/three-d-tiles-lyon-metropolis/Villeurbanne_GratteCiel_Temporal_2009-2012-2015-2018_TileSet/)

## Manual steps

Before starting:

- install [Docker](https://docs.docker.com/engine/install/)
- install [Docker Compose](https://docs.docker.com/compose/install/)
- install [3dcitydb/importer-exporter](https://github.com/3dcitydb/3dcitydb-suite/releases)
  - Note: make sure your release of the importer/exporter works with the latest image of the 3dcitydb docker

Using docker components from the [cityGMLto3DTiles](https://github.com/VCityTeam/cityGMLto3DTiles) repository the following pipeline can be realized

Docker images can be found [here](https://github.com/VCityTeam/cityGMLto3DTiles/tree/master/Docker) and can be built as follows:
```bash
git clone https://github.com/VCityTeam/cityGMLto3DTiles.git
docker build -t vcity/3duse cityGMLto3DTiles/Docker/3DUse-DockerContext
docker build -t vcity/citygml2stripper cityGMLto3DTiles/Docker/CityGML2Stripper-DockerContext
```

### Stage 0: obtain the reference original data

This boils down to importing data from [`dataset-dl.liris.cnrs.fr`](https://dataset-dl.liris.cnrs.fr/citygml-to-three-d-tiles-computations/stage_1/):

```bash
cd cityGMLto3DTiles
# Create all the output directories
mkdir stage_0 stage_1 stage_2 stage_3 stage_4 stage_5
cd stage_0
wget  https://dataset-dl.liris.cnrs.fr/citygml-to-three-d-tiles-computations/stage_1/2009/VILLEURBANNE_BATI_2009_patched.gml
wget  https://dataset-dl.liris.cnrs.fr/citygml-to-three-d-tiles-computations/stage_1/2012/VILLEURBANNE_BATI_2012_patched.gml
wget  https://dataset-dl.liris.cnrs.fr/citygml-to-three-d-tiles-computations/stage_1/2009/VILLEURBANNE_BATI_2009_alt_patched.gml
wget  https://dataset-dl.liris.cnrs.fr/citygml-to-three-d-tiles-computations/stage_1/2012/VILLEURBANNE_BATI_2012_alt_patched.gml
wget  https://dataset-dl.liris.cnrs.fr/citygml-to-three-d-tiles-computations/stage_1/2015/VILLEURBANNE_BATI_2015_patched.gml
wget  https://dataset-dl.liris.cnrs.fr/citygml-to-three-d-tiles-computations/stage_1/2018/VILLEURBANNE_BATI_2018_patched.gml
```

### Optional Stage: Data Cleaning
Some malformed geometry issues can cause problems during stages 2 and 3, to avoid this data cleaning may be required.
The [CityGMLPatcher](./CityGMLPatcher.py) python script can be used in conjunction with a CityDoctor2 output file.
For documentation on how to install and use CityDoctor2, see the CityDoctor2 [Website](https://projekt.bht-berlin.de/citydoctor2/downloads/) (recommended) or [Github](https://transfer.hft-stuttgart.de/gitlab/citydoctor/citydoctor2). Note that the CityGML patcher currently only works with CityGML 2.0 namespaces.

CityGMLPatcher documentation can be found using:
```bash
python CityGMLPatcher.py --help
```
For example:
```bash
python CityGMLPatcher.py \
   stage_0/VILLEURBANNE_BATI_2009.gml \
   2009-bat.xml \
   stage_1/VILLEURBANNE_BATI_2009_patched.gml \
   -i SE_ATTRIBUTE_MISSING
```
### Optional Stage: Extract Region of Interest
1. Edit the 4 password fields in the `.env` file with passwords of your choosing
2. Edit each `CityTilerDBConfig20xx.yml` file so that the password corresponds with what was set in step 1 
3. Launch the 4 3DCityDB docker containers with docker compose
```
docker-compose up
```
4. Launch 3dcitydb/importer-exporter and import each output from stage 3 into each corresponding database filtering out features outside of the following region of interest:
   - Xmin: 4.8742
   - Xmax: 4.8834
   - Ymin: 45.765
   - Ymax: 45.7735
### Stage 1: Strip Building Attributes

1. Place your CityGML datasets in a folder; for this example the folder refered to as `[host folder]`
2. Launch a CityGML2Stripper container with bash as the entrypoint
   ```bash
   docker run --rm --name cgmls1 -it --entrypoint /bin/bash -v [absolute-path-to-host-folder]:/io vcity/citygml2stripper
   ```
   e.g. for a bash shell
   ```bash
   docker run --rm --name cgmls1 -it --entrypoint /bin/bash -v $(pwd):/io vcity/citygml2stripper
   ```
3. From within the container's bash session, split the datasets output from `stage_1`:
   ```bash
   python /src/CityGML2Stripper.py --input /io/stage_1/[input-filename] --output /io/stage_2/[output-filename] --remove-building-parts
   ```
   e.g. (and all the successive inputs)
   ```bash
   python /src/CityGML2Stripper.py --input /io/stage_1/VILLEURBANNE_BATI_2009_patched.gml --output /io/stage_2/VILLEURBANNE_BATI_2009_stripped.gml --remove-building-parts
   python /src/CityGML2Stripper.py --input /io/stage_1/VILLEURBANNE_BATI_2012_patched.gml --output /io/stage_2/VILLEURBANNE_BATI_2012_stripped.gml --remove-building-parts
   python /src/CityGML2Stripper.py --input /io/stage_1/VILLEURBANNE_BATI_2009_alt_patched.gml --output /io/stage_2/VILLEURBANNE_BATI_2009_alt_stripped.gml --remove-building-parts
   python /src/CityGML2Stripper.py --input /io/stage_1/VILLEURBANNE_BATI_2012_alt_patched.gml --output /io/stage_2/VILLEURBANNE_BATI_2012_alt_stripped.gml --remove-building-parts
   python /src/CityGML2Stripper.py --input /io/stage_1/VILLEURBANNE_BATI_2015_patched.gml --output /io/stage_2/VILLEURBANNE_BATI_2015_stripped.gml --remove-building-parts
   python /src/CityGML2Stripper.py --input /io/stage_1/VILLEURBANNE_BATI_2018_patched.gml --output /io/stage_2/VILLEURBANNE_BATI_2018_stripped.gml --remove-building-parts
   ```
4. Repeat step 3 for each input file

### Stage 2: Split Buildings
1. Launch a 3DUse container with bash as the entrypoint
   ```bash
   docker run --rm --name 3duse1 -it --entrypoint /bin/bash -v [host folder]:/io vcity/3duse
   ```
   e.g. for a bash shell
   ```bash
   docker run --rm --name 3duse1 -it --entrypoint /bin/bash -v $(pwd):/io vcity/3duse
   ```
2. From within the container's bash session, split the dataset buildings:
   ```bash
   cd /root/3DUSE/Build/src/utils/cmdline/
   splitCityGMLBuildings --input-file /io/[input filename] --output-file /io/[output filename]
   ```
   e.g.
   ```bash
   cd /root/3DUSE/Build/src/utils/cmdline/;\
   splitCityGMLBuildings --input-file /io/stage_2/VILLEURBANNE_BATI_2009_stripped.gml --output-file /io/stage_3/VILLEURBANNE_BATI_2009_stripped.gml;\
   splitCityGMLBuildings --input-file /io/stage_2/VILLEURBANNE_BATI_2009_alt_stripped.gml --output-file /io/stage_3/VILLEURBANNE_BATI_2009_alt_stripped.gml;\
   splitCityGMLBuildings --input-file /io/stage_2/VILLEURBANNE_BATI_2012_stripped.gml --output-file /io/stage_3/VILLEURBANNE_BATI_2012_stripped.gml;\
   splitCityGMLBuildings --input-file /io/stage_2/VILLEURBANNE_BATI_2012_alt_stripped.gml --output-file /io/stage_3/VILLEURBANNE_BATI_2012_alt_stripped.gml
   ```
1. Repeat step 2 for each stage 1 vintage **before 2015**. 
   See [this comment](https://github.com/VCityTeam/cityGMLto3DTiles/blob/3c10f8235f6ab6c8a28df60f7b065ae8865b7623/PythonCallingDocker/demo_split_buildings.py#L32) for more info.
2. For vintages from 2015 and after simply copy the files and relabel them e.g.
   ```bash
   cp stage_2/VILLEURBANNE_BATI_2015_stripped.gml stage_3/VILLEURBANNE_BATI_2015_stripped_split.gml
   cp stage_2/VILLEURBANNE_BATI_2018_stripped.gml stage_3/VILLEURBANNE_BATI_2018_stripped_split.gml
   ```
3. Leave this console open to be reused in Stage 3

### Stage 3: Extract Building Dates (create change graphs with change detection)
1. Create the output directories of this stage
   ```bash
   mkdir stage_4/2009-2012-differences stage_4/2012-2015-differences stage_4/2015-2018-differences
   ```
2. From the 3DUse container's bash session, split the datasets output from stage 2:
   ```bash
   cd /root/3DUSE/Build/src/utils/cmdline/
   extractBuildingDates --first_date [1st input dataset year] \
                        --first_file /io/[1st input filename] \
                        --second_date [2nd input dataset year] \
                        --second_file /io/[2nd output filename] \
                        --output_dir /io/[[1st input dataset year]-[2nd input dataset year]]
   ```
   e.g. 
   ```bash
   extractBuildingDates --first_date 2009 --first_file /io/stage_3/VILLEURBANNE_BATI_2009_stripped_split.gml --second_date 2012 --second_file /io/stage_3/VILLEURBANNE_BATI_2012_stripped_split.gml --output_dir /io/stage_4/2009-2012-differences
   extractBuildingDates --first_date 2012 --first_file /io/stage_3/VILLEURBANNE_BATI_2012_stripped_split.gml --second_date 2015 --second_file /io/stage_3/VILLEURBANNE_BATI_2015_stripped_split.gml --output_dir /io/stage_4/2012-2015-differences
   extractBuildingDates --first_date 2015 --first_file /io/stage_3/VILLEURBANNE_BATI_2015_stripped_split.gml --second_date 2018 --second_file /io/stage_3/VILLEURBANNE_BATI_2018_stripped_split.gml --output_dir /io/stage_4/2015-2018-differences
   extractBuildingDates --first_date 2009 --first_file /io/stage_3/VILLEURBANNE_BATI_2009_stripped_split.gml --second_date 2010 --second_file /io/stage_3/VILLEURBANNE_BATI_2009_alt_stripped_split.gml --output_dir /io/stage_4/2009-2009alt-differences
   extractBuildingDates --first_date 2010 --first_file /io/stage_3/VILLEURBANNE_BATI_2009_alt_stripped_split.gml --second_date 2013 --second_file /io/stage_3/VILLEURBANNE_BATI_2012_alt_stripped_split.gml --output_dir /io/stage_4/2009alt-2012alt-differences
   extractBuildingDates --first_date 2013 --first_file /io/stage_3/VILLEURBANNE_BATI_2012_alt_stripped_split.gml --second_date 2015 --second_file /io/stage_3/VILLEURBANNE_BATI_2015_stripped_split.gml --output_dir /io/stage_4/2012alt-2015-differences
   ```
3. Repeat step 1 for each pair of sequential stage 2 output files and years:
   1. ```mermaid
      %%{init: {'gitGraph': {'mainBranchName': 'Scenario1'}} }%%
      gitGraph
         commit id: "2009"
         branch Scenario2
         commit id: "2009_alt"
         commit id: "2012_alt"
         checkout Scenario1
         commit id: "2012"
         merge Scenario2
         commit id: "2015"
         commit id: "2018"
      ```

### Stage 4 : Create and Load 3DCityDB Databases
1. Edit the 4 password fields in the `.env` file with passwords of your choosing
   - If this was already done in the optional stage 0, either a new `POSTGRES_DB_XXXX` variable must be declared for each database or the volumes for each database must be deleted to remove unstripped/unsplit CityGML buildings :
2. Edit each `CityTilerDBConfig20xx.yml` file so that the password corresponds with what was set in step 1 
3. Launch the 4 3DCityDB docker containers with docker compose
```
docker-compose up
```
1. Launch 3dcitydb/importer-exporter and import each output from stage 3 into each corresponding database filtering out features outside of the following region of interest:
   - Xmin: 4.8742
   - Xmax: 4.8834
   - Ymin: 45.765
   - Ymax: 45.7735

### Stage 5 : Create a 3DTiles tileset with a temporal extention
1. Install [py3dtilers](https://github.com/VCityTeam/py3dtilers#installation-from-sources) to create a 3DTile tileset with the data.
2. Once installed run the [CityTemporalTiler](https://github.com/VCityTeam/py3dtilers/tree/master/py3dtilers/CityTiler#citytemporaltiler-features).
   - Use the 4 `CityTilerDBConfig20xx.yml` files as the `-i` arguments.
   ```bash
   citygml-tiler-temporal \
      -i [path to this directory]/CityTilerDBConfig2009.yml \
         [path to this directory]/CityTilerDBConfig2012.yml \
         [path to this directory]/CityTilerDBConfig2015.yml \
         [path to this directory]/CityTilerDBConfig2018.yml \
      --time_stamps 2009 2012 2015 2018 \
      --temporal_graph [path to this directory]/stage_4/2009-2012-differences/DifferencesAsGraph.json \
                       [path to this directory]/stage_4/2012-2015-differences/DifferencesAsGraph.json \
                       [path to this directory]/stage_4/2015-2018-differences/DifferencesAsGraph.json
   ```
   e.g.
   ```bash
   citygml-tiler-temporal \
      -i ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2009.yml \
         ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2012.yml \
         ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2015.yml \
         ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2018.yml \
      --time_stamps 2009 2012 2015 2018 \
      --temporal_graph ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/stage_4/2009-2012-differences/DifferencesAsGraph.json \
                       ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/stage_4/2012-2015-differences/DifferencesAsGraph.json \
                       ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/stage_4/2015-2018-differences/DifferencesAsGraph.json
   ```
   and then:
      ```bash
   citygml-tiler-temporal \
      -i ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2009.yml \
         ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2009-alt.yml \
         ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2012-alt.yml \
         ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2015.yml \
         ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/CityTilerDBConfig2018.yml \
      --time_stamps 2009 2010 2013 2015 2018 \
      --temporal_graph ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/stage_4/2009-2009alt-differences/DifferencesAsGraph.json \
                       ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/stage_4/2009alt-2012alt-differences/DifferencesAsGraph.json \
                       ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/stage_4/2012alt-2015-differences/DifferencesAsGraph.json \
                       ../UD-Reproducibility/Computations/3DTiles/GratteCielTemporal2009-2018/stage_4/2015-2018-differences/DifferencesAsGraph.json
   ```
   