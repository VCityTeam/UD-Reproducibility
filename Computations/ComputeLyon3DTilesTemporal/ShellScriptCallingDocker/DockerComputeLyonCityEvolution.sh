# !/bin/sh

# This script detects the changes between CityGML files representing the
# buildings of the city of Lyon at two different vintages and outputs the
# changes as graphML-JSON files.

# Awaited parameters:
# * output folder for the intermdiate data and for the final result.

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# Check that parameters are correctly provided
if [ $# != 1 ]
  then
	  echo "Awaited parameters: output folder."
    exit 1
fi

######## Configure what needs to be (with j2cli)
echo "--- Configuring data base servers (and clients)"
j2 3dCityDBImpExpConfig.j2 DBConfig2009.yml -o 3dCityDBImpExpConfig-2009.xml
j2 3dCityDBImpExpConfig.j2 DBConfig2012.yml -o 3dCityDBImpExpConfig-2012.xml
j2 3dCityDBImpExpConfig.j2 DBConfig2015.yml -o 3dCityDBImpExpConfig-2015.xml

j2 LaunchDataBaseSingleServer.sh.j2 DBConfig2009.yml -o LaunchDataBaseServerFirst.sh
j2 LaunchDataBaseSingleServer.sh.j2 DBConfig2012.yml -o LaunchDataBaseServerSecond.sh
j2 LaunchDataBaseSingleServer.sh.j2 DBConfig2015.yml -o LaunchDataBaseServerThird.sh

# RunTiler.sh configuration files are in yaml format
cp DBConfig2009.yml ../Docker/CityTiler-DockerContext/CityTilerDBConfig2009.yml
cp DBConfig2012.yml ../Docker/CityTiler-DockerContext/CityTilerDBConfig2012.yml
cp DBConfig2015.yml ../Docker/CityTiler-DockerContext/CityTilerDBConfig2015.yml

# Create output directory
mkdir ${1}

if false; then
##########
echo "--- Download and patch the original data"
# For the city of Lyon (years 2009, 2012 and 2015) we use the
# [Data Grand Lyon open portal](https://data.grandlyon.com/) and patch the
# errors in the files (e.g. buildings with empty geometry and textures with
# wrong coordinates).
./DockerDownloadPatchLyonCityGML.sh 2009 ${1}/Lyon_2009
./DockerDownloadPatchLyonCityGML.sh 2012 ${1}/Lyon_2012
./DockerDownloadPatchLyonCityGML.sh 2015 ${1}/Lyon_2015

##########
echo "--- Spliting buildings (when required)"
# Building split is only required for the years 2009 and 2012 since 2015 buildings
# are alreading properly "splitted":
./DockerSplitBuildingsLyonCityGML.sh ${1}/Lyon_2009 2009 ${1}/Lyon_2009_Splitted
./DockerSplitBuildingsLyonCityGML.sh ${1}/Lyon_2012 2012 ${1}/Lyon_2012_Splitted

# For 2015 we simply re-cast the file hierachy out of the original GrandLyon
# folders organization
mkdir ${1}/Lyon_2015_Splitted
cp ${1}/Lyon_2015/LYON_1ER_2015/LYON_1ER_BATI_2015.gml   ${1}/Lyon_2015_Splitted
cp ${1}/Lyon_2015/LYON_2EME_2015/LYON_2EME_BATI_2015.gml ${1}/Lyon_2015_Splitted
cp ${1}/Lyon_2015/LYON_3EME_2015/LYON_3EME_BATI_2015.gml ${1}/Lyon_2015_Splitted
cp ${1}/Lyon_2015/LYON_4EME_2015/LYON_4EME_BATI_2015.gml ${1}/Lyon_2015_Splitted
cp ${1}/Lyon_2015/LYON_5EME_2015/LYON_5EME_BATI_2015.gml ${1}/Lyon_2015_Splitted
cp ${1}/Lyon_2015/LYON_6EME_2015/LYON_6EME_BATI_2015.gml ${1}/Lyon_2015_Splitted
cp ${1}/Lyon_2015/LYON_7EME_2015/LYON_7_BATI_2015.gml    ${1}/Lyon_2015_Splitted/LYON_7EME_BATI_2015.gml
cp ${1}/Lyon_2015/LYON_8EME_2015/LYON_8EME_BATI_2015.gml ${1}/Lyon_2015_Splitted
cp ${1}/Lyon_2015/LYON_9EME_2015/LYON_9EME_BATI_2015.gml ${1}/Lyon_2015_Splitted

##########
echo "--- Stripping Appearance attributes"
./DockerStripAttributes.sh ${1}/Lyon_2009_Splitted 2009 ${1}/Lyon_2009_Splitted_Stripped
./DockerStripAttributes.sh ${1}/Lyon_2012_Splitted 2012 ${1}/Lyon_2012_Splitted_Stripped
./DockerStripAttributes.sh ${1}/Lyon_2015_Splitted 2015 ${1}/Lyon_2015_Splitted_Stripped

##########
echo "--- Detect changes between two (consecutive) vintages of the city"
./DockerExtractBuildingDates.sh 2009 ${1}/Lyon_2009_Splitted \
                                2012 ${1}/Lyon_2012_Splitted \
                                ${1}/2009_2012_Differences
./DockerExtractBuildingDates.sh 2012 ${1}/Lyon_2012_Splitted \
                                2015 ${1}/Lyon_2015_Splitted \
                                ${1}/2012_2015_Differences

fi
###### Launch the 3dcitydb-postgis database servers
./LaunchDataBaseServers.sh

###### Load the databases
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2009 3dCityDBImpExpConfig-2009.xml ${1}/Lyon_2009_Splitted_Stripped
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2012 3dCityDBImpExpConfig-2012.xml ${1}/Lyon_2012_Splitted_Stripped
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2015 3dCityDBImpExpConfig-2015.xml ${1}/Lyon_2015_Splitted_Stripped

###### Preparing data for tile-set computation
copy_difference_files_from_dir() {
  # First argument: source directory
  # Second argument: target directory
  for i in $( ls ${1} ); do
    filename=${1}/${i}/DifferencesAsGraph.json
    if [ -f ${filename} ]; then
      cp ${1}/${i}/DifferencesAsGraph.json ${2}/${i}-DifferencesAsGraph.json
    else
      echo "WARNING: unfound difference file ", ${filename}
    fi 
  done
}

mkdir -p ${1}/Differences
copy_difference_files_from_dir ${1}/2009_2012_Differences ${1}/Differences
copy_difference_files_from_dir ${1}/2012_2015_Differences ${1}/Differences

###### Compute the resulting tile-set
echo "--- Running the tileset computation per se"
./RunTiler.sh ${1}/Differences ${1}/Result

###### Hald the 3dcitydb-postgis database servers
./HaltDataBaseServers.sh
