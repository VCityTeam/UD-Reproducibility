# !/bin/sh

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# This script strips the CityGML files some un-necessary attibutes.

if [ $# != 2 ]; then
    echo "Two parameters must be provided to this script:"
    echo "  1. the output folder holding the computed tileset."
    echo "  2. the database server configuration file."
    echo "Note: the rest i.e. almost everything is alas hardwired."
    exit 1
fi

# Note: if you wonder where the configuration files of the form
# CityTilerDBConfigYYYY.yml (that end up in Docker/CityTiler-DockerContext/)
# might come from then look in the configuration section of
# ComputeLyonCityEvolution.sh

pushd Docker/
docker build -t liris:Py3dTilesTiler CityTiler-DockerContext
popd

run_docker() {
  docker run \
    --mount src=`pwd`/$1,target=/Output,type=bind \
    -t liris:Py3dTilesTiler \
    Tiler $2 
}

mkdir -p $1
# A single run gathers it all in a single Temporal tileset:
run_docker $1 $2
