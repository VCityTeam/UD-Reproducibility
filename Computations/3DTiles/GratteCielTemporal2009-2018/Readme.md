# Change Detection Pipeline
This is a manual calculation of a 3DTiles+temporal extention of a small data set of the Gratte Ciel neighborhood

## Manual steps
Before starting, [install Docker](https://docs.docker.com/engine/install/) 

Using docker components from the [cityGMLto3DTiles](https://github.com/VCityTeam/cityGMLto3DTiles) repository the following pipeline can be realized

Docker images can be found [here](https://github.com/VCityTeam/cityGMLto3DTiles/tree/master/Docker) and can be built as follows:
```bash
git clone https://github.com/VCityTeam/cityGMLto3DTiles.git
docker build -t vcity/citytiler cityGMLto3DTiles/Docker/CityTiler-DockerContext
docker build -t vcity/3duse cityGMLto3DTiles/Docker/3DUse-DockerContext
docker build -t vcity/citygml2stripper cityGMLto3DTiles/Docker/CityGML2Stripper-DockerContext
```

### Stage 1: Strip Building Attributes
1. Place your CityGML datasets in a folder; for this example the folder refered to as `[host folder]`
2. Launch a CityGML2Stripper-Docker shell console
```bash
docker run --name cgmls1 -it --entrypoint /bin/bash -v [host folder]:/io vcity/citygml2stripper
```
3. From the container's shell console, split the datasets output from stage 1:
```bash
python /src/CityGML2Stripper.py --input /io/[input filename] --output /io/[output filename] --remove-building-parts
```
4. Repeat step 3 for each input file

### Stage 2: Split Buildings
1. Launch a 3DUse-Docker shell console
```bash
docker run --name 3duse1 -it --entrypoint /bin/bash -v [host folder]:/io vcity/3duse
```
2. From the container's shell console, split the dataset buildings:
```bash
cd /root/3DUSE/Build/src/utils/cmdline/
splitCityGMLBuildings --input-file /io/[input filename] --output-file /io/[output filename]
```
4. Repeat step 2 for each stage 1 output file
5. Leave this console open to be reused in Stage 3

### Stage 3: Extract Building Dates (create change graphs with change detection)
1. From the 3DUse-Docker shell console, split the datasets output from stage 2:
```bash
cd /root/3DUSE/Build/src/utils/cmdline/
extractBuildingDates --first_date [1st input dataset year] \
                     --first_file /io/[1st input filename] \
                     --second_date [2nd input dataset year] \
                     --second_file /io/[2nd output filename] \
                     --output_dir /io/
```
3. Repeat step 1 for each pair of sequential stage 2 output files and years

### Stage 4: Create a 3DTiles tileset
