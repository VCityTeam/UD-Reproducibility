# !/bin/sh

# This script detects the changes between CityGML files representing the
# buildings of the city of Lyon at two different vintages and outputs the
# changes as graphML-JSON files.

# Exit on first trouble 
set -e

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# Check that parameters are correctly provided
if [ $# != 1 ]
  then
    echo "Awaited parameters: output folder for the intermediate and final data."
    exit 1
fi

########## Create output directory
cd ../Shared
# Directory standing within ../Shared
temp_dir=temp_output/${1}
mkdir -p ${temp_dir}

######## Configure what needs to be (with j2cli)
echo "--- Configuring"
j2 Configure.sh.j2 DBConfig2009.yml -o Configure-2009.sh
j2 Configure.sh.j2 DBConfig2012.yml -o Configure-2012.sh
j2 Configure.sh.j2 DBConfig2015.yml -o Configure-2015.sh
chmod a+x Configure-2009.sh Configure-2012.sh Configure-2015.sh
./Configure-2009.sh
./Configure-2012.sh
./Configure-2015.sh
echo "--- Done"
echo ""

##########
echo "--- Download and patch the original data"
# For the city of Lyon we use the
# [Data Grand Lyon open portal](https://data.grandlyon.com/) and patch the
# errors in the files (e.g. buildings with empty geometry and textures with
# wrong coordinates).
./DockerDownloadPatchLyonCityGML.sh 2009 ${temp_dir}/Lyon_2009
./DockerDownloadPatchLyonCityGML.sh 2012 ${temp_dir}/Lyon_2012
./DockerDownloadPatchLyonCityGML.sh 2015 ${temp_dir}/Lyon_2015
echo "--- Done"
echo ""

##########
echo "--- Spliting buildings (when required)"
./DockerSplitBuildingsLyonCityGML.sh ${temp_dir}/Lyon_2009 2009 ${temp_dir}/Lyon_2009_Splitted
./DockerSplitBuildingsLyonCityGML.sh ${temp_dir}/Lyon_2012 2012 ${temp_dir}/Lyon_2012_Splitted
./SplitBuildingsLyonCityGML2015.sh ${temp_dir}/Lyon_2015  ${temp_dir}/Lyon_2015_Splitted
echo "--- Done"
echo ""

##########
echo "--- Stripping Appearance attributes"
./DockerStripAttributes.sh ${temp_dir}/Lyon_2009_Splitted 2009 ${temp_dir}/Lyon_2009_Splitted_Stripped
./DockerStripAttributes.sh ${temp_dir}/Lyon_2012_Splitted 2012 ${temp_dir}/Lyon_2012_Splitted_Stripped
./DockerStripAttributes.sh ${temp_dir}/Lyon_2015_Splitted 2015 ${temp_dir}/Lyon_2015_Splitted_Stripped
echo "--- Done"
echo ""

##########
echo "--- Detect changes between two (consecutive) vintages of the city"
./DockerExtractBuildingDates.sh 2009 ${temp_dir}/Lyon_2009_Splitted \
                                2012 ${temp_dir}/Lyon_2012_Splitted \
                                ${temp_dir}/2009_2012_Differences
./DockerExtractBuildingDates.sh 2012 ${temp_dir}/Lyon_2012_Splitted \
                                2015 ${temp_dir}/Lyon_2015_Splitted \
                                ${temp_dir}/2012_2015_Differences
echo "--- Done"
echo ""

###### Launch the 3dcitydb-postgis database server
echo "--- Launching the database server"
./LaunchDataBaseServer2009.sh
./LaunchDataBaseServer2012.sh
./LaunchDataBaseServer2015.sh
echo "   Waiting 60' for tumgis/3dcitydb-postgis to spin off ..."
sleep 60
echo "--- Done"
echo ""

###### Load the databases
echo "--- Loading the database"
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2009 3dCityDBImpExpConfig-2009.xml ${temp_dir}/Lyon_2009_Splitted_Stripped
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2012 3dCityDBImpExpConfig-2012.xml ${temp_dir}/Lyon_2012_Splitted_Stripped
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2015 3dCityDBImpExpConfig-2015.xml ${temp_dir}/Lyon_2015_Splitted_Stripped
echo "--- Done"
echo ""

###### Preparing data for tile-set computation
echo "--- Preparing data for tile-set computation"
copy_difference_files_from_dir() {
  # First argument: source directory
  # Second argument: target directory
  for i in $( ls ${1} ); do
    filename=${1}/${i}/DifferencesAsGraph.json
    if [ -f ${filename} ]; then
      cp ${filename} ${2}/${i}-DifferencesAsGraph.json
    else
      echo "WARNING: unfound difference file ", ${filename}
    fi 
  done
}

mkdir -p ${temp_dir}/Differences
copy_difference_files_from_dir ${temp_dir}/2009_2012_Differences ${temp_dir}/Differences
copy_difference_files_from_dir ${temp_dir}/2012_2015_Differences ${temp_dir}/Differences
echo "--- Done"
echo ""

###### Compute the resulting tile-set
echo "--- Running the tileset computation per se"
./RunTemporalTiler.sh ${temp_dir}/Result \
  CityTilerDBConfig2009.yml CityTilerDBConfig2012.yml CityTilerDBConfig2015.yml \
  ${temp_dir}/Differences

###### Halt the 3dcitydb-postgis database server
echo "--- Halting the database server."
./HaltDataBaseServer2009.sh
./HaltDataBaseServer2012.sh
./HaltDataBaseServer2015.sh
echo "--- Done"
echo ""

###### Eventually we move back the result to the directory holding this script
mv ${temp_dir} ../Temporal/
