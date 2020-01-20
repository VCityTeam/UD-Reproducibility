# !/bin/sh

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

########## Create output directory
# Directory standing within ../Shared
temp_dir=temp_output/${1}
mkdir -p ${temp_dir}

######## Configure what needs to be (with j2cli)
echo "--- Configuring"
j2 Configure.sh.j2 DBConfig2009.yml -o Configure-2009.sh
chmod a+x Configure-2009.sh
./Configure-2009.sh

##########
echo "--- Download and patch the original data"
# For the city of Lyon we use the
# [Data Grand Lyon open portal](https://data.grandlyon.com/) and patch the
# errors in the files (e.g. buildings with empty geometry and textures with
# wrong coordinates).
./DockerDownloadPatchLyonCityGML.sh 2009 ${temp_dir}/Lyon_2009

##########
echo "--- Spliting buildings (when required)"
# Building split is only required for the years 2009 and 2012 since 2015 buildings
# are alreading properly "splitted":
./DockerSplitBuildingsLyonCityGML.sh ${temp_dir}/Lyon_2009 2009 ${temp_dir}/Lyon_2009_Splitted

##########
echo "--- Stripping Appearance attributes"
./DockerStripAttributes.sh ${temp_dir}/Lyon_2009_Splitted 2009 ${temp_dir}/Lyon_2009_Splitted_Stripped

###### Launch the 3dcitydb-postgis database server
./LaunchDataBaseServer2009.sh
echo -n "   Waiting for tumgis/3dcitydb-postgis to spin off..."
sleep 10
echo "done."

###### Load the databases
./DockerLoad3dCityDataBase.sh citydb-full_lyon-2009 3dCityDBImpExpConfig-2009.xml ${temp_dir}/Lyon_2009_Splitted_Stripped

###### Compute the resulting tile-set
echo "--- Running the tileset computation per se"
./RunStaticTiler.sh ${temp_dir}/Result

###### Hald the 3dcitydb-postgis database servers
./HaltDataBaseServer2009.sh

###### Eventually we move back the result to the directory holding this script
mv ${temp_dir} ../Lyon2009/
