# Temporal Tileset for Gratte Ciel
This is a manual calculation of a 3DTiles+temporal extention of a small data set of the Gratte Ciel neighborhood

The input and the output data for each stage - as calculated thus - far can be found on [nextcloud](https://partage.liris.cnrs.fr/index.php/f/151016)

## Manual steps
Before starting:
- install [Docker](https://docs.docker.com/engine/install/)
- install [Docker Compose](https://docs.docker.com/compose/install/)
- install [3dcitydb/importer-exporter v5.0.0](https://github.com/3dcitydb/3dcitydb-suite/releases/tag/v2021.1.0) (this version will work with 3DCityDB 4.2.0)


Using docker components from the [cityGMLto3DTiles](https://github.com/VCityTeam/cityGMLto3DTiles) repository the following pipeline can be realized

Docker images can be found [here](https://github.com/VCityTeam/cityGMLto3DTiles/tree/master/Docker) and can be built as follows:
```bash
git clone https://github.com/VCityTeam/cityGMLto3DTiles.git
docker build -t vcity/3duse cityGMLto3DTiles/Docker/3DUse-DockerContext
docker build -t vcity/citygml2stripper cityGMLto3DTiles/Docker/CityGML2Stripper-DockerContext
```

### Stage 1: Strip Building Attributes
1. Place your CityGML datasets in a folder; for this example the folder refered to as `[host folder]`
2. Launch a CityGML2Stripper container with bash as the entrypoint
```bash
docker run --name cgmls1 -it --entrypoint /bin/bash -v [host folder]:/io vcity/citygml2stripper
```
3. From within the container's bash session, split the datasets output from stage 1:
```bash
python /src/CityGML2Stripper.py --input /io/[input filename] --output /io/[output filename] --remove-building-parts
```
4. Repeat step 3 for each input file

### Stage 2: Split Buildings
1. Launch a 3DUse container with bash as the entrypoint
```bash
docker run --name 3duse1 -it --entrypoint /bin/bash -v [host folder]:/io vcity/3duse
```
2. From within the container's bash session, split the dataset buildings:
```bash
cd /root/3DUSE/Build/src/utils/cmdline/
splitCityGMLBuildings --input-file /io/[input filename] --output-file /io/[output filename]
```
4. Repeat step 2 for each stage 1 vintage **before 2015**. See [this comment](https://github.com/VCityTeam/cityGMLto3DTiles/blob/3c10f8235f6ab6c8a28df60f7b065ae8865b7623/PythonCallingDocker/demo_split_buildings.py#L32) for more info.
5. Leave this console open to be reused in Stage 3

### Stage 3: Extract Building Dates (create change graphs with change detection)
1. From the 3DUse container's bash session, split the datasets output from stage 2:
```bash
cd /root/3DUSE/Build/src/utils/cmdline/
extractBuildingDates --first_date [1st input dataset year] \
                     --first_file /io/[1st input filename] \
                     --second_date [2nd input dataset year] \
                     --second_file /io/[2nd output filename] \
                     --output_dir /io/[[1st input dataset year]-[2nd input dataset year]]
```
2. Repeat step 1 for each pair of sequential stage 2 output files and years

### Stage 4 : Create and Load 3DCityDB Databases
1. Edit the 4 password fields in the `.env` file with passwords of your choosing
2. Edit each `CityTilerDBConfig20xx.yml` file so that the password corresponds with what was set in step 1 
3. Launch the 4 3DCityDB docker containers with docker compose
```
docker-compose up
```
4. Launch 3dcitydb/importer-exporter and load each output from stage 3 into each corresponding database 

### Stage 5 : Create a 3DTiles tileset with a temporal extention
1. Install [py3dtilers](https://github.com/VCityTeam/py3dtilers#installation-from-sources) to create a 3DTile tileset with the data.
2. Once installed run the [CityTemporalTiler](https://github.com/VCityTeam/py3dtilers/tree/master/py3dtilers/CityTiler#citytemporaltiler-features).
   - Use the 4 `CityTilerDBConfig20xx.yml` files as the `--db_config_path` arguments.
```
citygml-tiler-temporal                                         \
  --db_config_path [Path to config]/CityTilerDBConfig2009.yml  \
                   [Path to config]/CityTilerDBConfig2012.yml  \
                   [Path to config]/CityTilerDBConfig2015.yml  \
                   [Path to config]/CityTilerDBConfig2018.yml  \
  --time_stamps 2009 2012 2015 2018                            \
  --temporal_graph [host folder]/2009-2012/DifferencesAsGraph.json  \
                   [host folder]/2012-2015/DifferencesAsGraph.json  \
                   [host folder]/2015-2018/DifferencesAsGraph.json
```
