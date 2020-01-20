# !/bin/sh

# This script detects the changes between CityGML files representing the
# buildings of the city of Lyon at two different vintages and outputs the
# changes as graphML-JSON files.

# Awaited parameters:
# * output folder for the intermdiate data and for the final result.

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit
cd ../Shared

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

j2   LaunchDataBaseSingleServer.sh.j2 DBConfig2009.yml \
  -o LaunchDataBaseServerFirst.sh
j2   LaunchDataBaseSingleServer.sh.j2 DBConfig2012.yml \
  -o LaunchDataBaseServerSecond.sh
j2   LaunchDataBaseSingleServer.sh.j2 DBConfig2015.yml \
  -o LaunchDataBaseServerThird.sh
chmod a+x LaunchDataBaseServerFirst.sh \
          LaunchDataBaseServerSecond.sh \
          LaunchDataBaseServerThird.sh

j2   HaltDataBaseSingleServer.sh.j2 DBConfig2009.yml \
  -o HaltDataBaseServerFirst.sh
j2   HaltDataBaseSingleServer.sh.j2 DBConfig2012.yml \
  -o HaltDataBaseServerSecond.sh
j2   HaltDataBaseSingleServer.sh.j2 DBConfig2015.yml \
  -o HaltDataBaseServerThird.sh
chmod a+x HaltDataBaseServerFirst.sh \
          HaltDataBaseServerSecond.sh \
          HaltDataBaseServerThird.sh

# RunTiler.sh configuration files are in yaml format
cp DBConfig2009.yml Docker/CityTiler-DockerContext/CityTilerDBConfig2009.yml
cp DBConfig2012.yml Docker/CityTiler-DockerContext/CityTilerDBConfig2012.yml
cp DBConfig2015.yml Docker/CityTiler-DockerContext/CityTilerDBConfig2015.yml

# Directory standing within ../Shared
temp_dir=temp_output/${1}
mkdir -p ${temp_dir}

##########
echo "--- Download and patch the original data"
# For the city of Lyon (years 2009, 2012 and 2015) we use the
# [Data Grand Lyon open portal](https://data.grandlyon.com/) and patch the
# errors in the files (e.g. buildings with empty geometry and textures with
# wrong coordinates).
./DockerDownloadPatchLyonCityGML.sh 2009 ${temp_dir}/Lyon_2009
./DockerDownloadPatchLyonCityGML.sh 2012 ${temp_dir}/Lyon_2012
./DockerDownloadPatchLyonCityGML.sh 2015 ${temp_dir}/Lyon_2015

##########
echo "--- Spliting buildings (when required)"
# Building split is only required for the years 2009 and 2012 since 2015 buildings
# are alreading properly "splitted":
./DockerSplitBuildingsLyonCityGML.sh ${temp_dir}/Lyon_2009 2009 ${temp_dir}/Lyon_2009_Splitted
./DockerSplitBuildingsLyonCityGML.sh ${temp_dir}/Lyon_2012 2012 ${temp_dir}/Lyon_2012_Splitted

# For 2015 we simply re-cast the file hierachy out of the original GrandLyon
# folders organization
mkdir ${temp_dir}/Lyon_2015_Splitted
cp ${temp_dir}/Lyon_2015/LYON_1ER_2015/LYON_1ER_BATI_2015.gml   ${temp_dir}/Lyon_2015_Splitted
cp ${temp_dir}/Lyon_2015/LYON_2EME_2015/LYON_2EME_BATI_2015.gml ${temp_dir}/Lyon_2015_Splitted
cp ${temp_dir}/Lyon_2015/LYON_3EME_2015/LYON_3EME_BATI_2015.gml ${temp_dir}/Lyon_2015_Splitted
cp ${temp_dir}/Lyon_2015/LYON_4EME_2015/LYON_4EME_BATI_2015.gml ${temp_dir}/Lyon_2015_Splitted
cp ${temp_dir}/Lyon_2015/LYON_5EME_2015/LYON_5EME_BATI_2015.gml ${temp_dir}/Lyon_2015_Splitted
cp ${temp_dir}/Lyon_2015/LYON_6EME_2015/LYON_6EME_BATI_2015.gml ${temp_dir}/Lyon_2015_Splitted
cp ${temp_dir}/Lyon_2015/LYON_7EME_2015/LYON_7_BATI_2015.gml    ${temp_dir}/Lyon_2015_Splitted/LYON_7EME_BATI_2015.gml
cp ${temp_dir}/Lyon_2015/LYON_8EME_2015/LYON_8EME_BATI_2015.gml ${temp_dir}/Lyon_2015_Splitted
cp ${temp_dir}/Lyon_2015/LYON_9EME_2015/LYON_9EME_BATI_2015.gml ${temp_dir}/Lyon_2015_Splitted

##########
echo "--- Stripping Appearance attributes"
./DockerStripAttributes.sh ${temp_dir}/Lyon_2009_Splitted 2009 ${temp_dir}/Lyon_2009_Splitted_Stripped
./DockerStripAttributes.sh ${temp_dir}/Lyon_2012_Splitted 2012 ${temp_dir}/Lyon_2012_Splitted_Stripped
./DockerStripAttributes.sh ${temp_dir}/Lyon_2015_Splitted 2015 ${temp_dir}/Lyon_2015_Splitted_Stripped

##########
echo "--- Detect changes between two (consecutive) vintages of the city"
./DockerExtractBuildingDates.sh 2009 ${temp_dir}/Lyon_2009_Splitted \
                                2012 ${temp_dir}/Lyon_2012_Splitted \
                                ${temp_dir}/2009_2012_Differences
./DockerExtractBuildingDates.sh 2012 ${temp_dir}/Lyon_2012_Splitted \
                                2015 ${temp_dir}/Lyon_2015_Splitted \
                                ${temp_dir}/2012_2015_Differences

###### Launch the 3dcitydb-postgis database servers
./LaunchDataBaseServers.sh

###### Load the databases
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2009 3dCityDBImpExpConfig-2009.xml ${temp_dir}/Lyon_2009_Splitted_Stripped
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2012 3dCityDBImpExpConfig-2012.xml ${temp_dir}/Lyon_2012_Splitted_Stripped
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2015 3dCityDBImpExpConfig-2015.xml ${temp_dir}/Lyon_2015_Splitted_Stripped

###### Preparing data for tile-set computation
copy_difference_files_from_dir() {
  # First argument: source directory
  # Second argument: target directory
  for i in $( ls ${temp_dir} ); do
    filename=${temp_dir}/${i}/DifferencesAsGraph.json
    if [ -f ${filename} ]; then
      cp ${temp_dir}/${i}/DifferencesAsGraph.json ${2}/${i}-DifferencesAsGraph.json
    else
      echo "WARNING: unfound difference file ", ${filename}
    fi 
  done
}

mkdir -p ${temp_dir}/Differences
copy_difference_files_from_dir ${temp_dir}/2009_2012_Differences ${temp_dir}/Differences
copy_difference_files_from_dir ${temp_dir}/2012_2015_Differences ${temp_dir}/Differences

###### Compute the resulting tile-set
echo "--- Running the tileset computation per se"
./RunTemporalTiler.sh ${temp_dir}/Differences ${temp_dir}/Result

###### Hald the 3dcitydb-postgis database servers
./HaltDataBaseServers.sh

# Eventually we move back the result to the directory holding this script
output_dir=../Temporal/${1}
mkdir -p ${output_dir}
mv ${temp_dir}/Lyon_2009 ${output_dir}
