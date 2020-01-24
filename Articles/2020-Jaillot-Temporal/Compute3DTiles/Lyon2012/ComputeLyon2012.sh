# !/bin/sh

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
j2 Configure.sh.j2 DBConfig2012.yml -o Configure-2012.sh
chmod a+x Configure-2012.sh
./Configure-2012.sh

##########
echo "--- Download and patch the original data"
# For the city of Lyon we use the
# [Data Grand Lyon open portal](https://data.grandlyon.com/) and patch the
# errors in the files (e.g. buildings with empty geometry and textures with
# wrong coordinates).
./DockerDownloadPatchLyonCityGML.sh 2012 ${temp_dir}/Lyon_2012

##########
echo "--- Spliting buildings (when required)"
./DockerSplitBuildingsLyonCityGML.sh ${temp_dir}/Lyon_2012 2012 ${temp_dir}/Lyon_2012_Splitted

##########
echo "--- Stripping Appearance attributes"
./DockerStripAttributes.sh ${temp_dir}/Lyon_2012_Splitted 2012 ${temp_dir}/Lyon_2012_Splitted_Stripped

###### Launch the 3dcitydb-postgis database server
./LaunchDataBaseServer2012.sh
echo -n "   Waiting 30' for tumgis/3dcitydb-postgis to spin off ..."
sleep 30
echo "done."

###### Load the databases
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2012 3dCityDBImpExpConfig-2012.xml ${temp_dir}/Lyon_2012_Splitted_Stripped

###### Compute the resulting tile-set
echo "--- Running the tileset computation per se"
./RunStaticTiler.sh ${temp_dir}/Result CityTilerDBConfig2012.yml

###### Hald the 3dcitydb-postgis database servers
./HaltDataBaseServer2012.sh

###### Eventually we move back the result to the directory holding this script
mv ${temp_dir} ../Lyon2012/

###### Checking result validity
# ./validate_checksum.sh "Result/tileset_ouput_dir"
