# !/bin/sh

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# This script strips the CityGML files some un-necessary attibutes.

# Check that parameters are correctly provided
if [ $# != 3 ]
  then
    echo "Three parameters must be provided to this script:"
    echo "  1. input folder (a folder containing the CityGML data of all the"
    echo "     boroughs of the city of Lyon for a given year like the one"
    echo "     produced by e.g. the script DockerSplitBuildingsLyonCityGML.sh),"
    echo "  2. year (of the city of Lyon represented by the CityGML files),"
    echo "  3. the name of the output folder with the resulting striped files" 
    exit 1
fi

pushd ../Docker/
docker build -t liris:CityGML2Stripper CityGML2Stripper-DockerContext
popd

mkdir $3

run_docker() {
  echo "Stripping Appearance attributes from file $1"
  docker run \
    --mount src=`pwd`,target=/Input,type=bind \
    --mount src=`pwd`,target=/Output,type=bind \
    -t liris:CityGML2Stripper \
    --input /Input/$1 --output /Output/$2
}

# Split buildings of all Lyon Borrough
run_docker ${1}/LYON_1ER_BATI_${2}.gml  ${3}/LYON_1ER_BATI_${2}.gml
run_docker ${1}/LYON_2EME_BATI_${2}.gml ${3}/LYON_2EME_BATI_${2}.gml
run_docker ${1}/LYON_3EME_BATI_${2}.gml ${3}/LYON_3EME_BATI_${2}.gml
run_docker ${1}/LYON_4EME_BATI_${2}.gml ${3}/LYON_4EME_BATI_${2}.gml
run_docker ${1}/LYON_5EME_BATI_${2}.gml ${3}/LYON_5EME_BATI_${2}.gml
run_docker ${1}/LYON_6EME_BATI_${2}.gml ${3}/LYON_6EME_BATI_${2}.gml
run_docker ${1}/LYON_7EME_BATI_${2}.gml ${3}/LYON_7EME_BATI_${2}.gml
run_docker ${1}/LYON_8EME_BATI_${2}.gml ${3}/LYON_8EME_BATI_${2}.gml
run_docker ${1}/LYON_9EME_BATI_${2}.gml ${3}/LYON_9EME_BATI_${2}.gml
