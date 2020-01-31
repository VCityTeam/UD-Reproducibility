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
j2 Configure.sh.j2 DBConfig2009.yml -o Configure-2009.sh
chmod a+x Configure-2009.sh
./Configure-2009.sh
echo "--- Done"
echo ""

##########
echo "--- Download and patch the original data"
# For the city of Lyon we use the
# [Data Grand Lyon open portal](https://data.grandlyon.com/) and patch the
# errors in the files (e.g. buildings with empty geometry and textures with
# wrong coordinates).
./DockerDownloadPatchLyonCityGML.sh 2009 ${temp_dir}/Lyon_2009
echo "--- Done"
echo ""

##########
echo "--- Spliting buildings (when required)"
./DockerSplitBuildingsLyonCityGML.sh ${temp_dir}/Lyon_2009 2009 ${temp_dir}/Lyon_2009_Splitted
echo "--- Done"
echo ""

##########
echo "--- Stripping Appearance attributes"
./DockerStripAttributes.sh ${temp_dir}/Lyon_2009_Splitted 2009 ${temp_dir}/Lyon_2009_Splitted_Stripped
echo "--- Done"
echo ""

###### Launch the 3dcitydb-postgis database server
echo "--- Launching the database server"
./LaunchDataBaseServer2009.sh
echo -n "   Waiting 60' for tumgis/3dcitydb-postgis to spin off ..."
sleep 60
echo "--- Done"
echo ""

###### Load the databases
echo "--- Loading the database"
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2009 3dCityDBImpExpConfig-2009.xml ${temp_dir}/Lyon_2009_Splitted_Stripped
echo "--- Done"
echo ""

###### Compute the resulting tile-set
echo "--- Running the tileset computation per se"
./RunStaticTiler.sh ${temp_dir}/Result CityTilerDBConfig2009.yml
echo "--- Done"
echo ""

###### Halt the 3dcitydb-postgis database server
echo "--- Halting the database server."
./HaltDataBaseServer2009.sh
echo "--- Done"
echo ""

###### Eventually we move back the result to the directory holding this script
mv ${temp_dir} ../Lyon2009/

###### Checking result validity
# ./validate_checksum.sh "Result/tileset_ouput_dir"
