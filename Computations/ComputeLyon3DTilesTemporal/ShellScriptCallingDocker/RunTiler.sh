#!/bin/bash

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# This script strips the CityGML files some un-necessary attibutes.

if [ $# != 2 ]; then
    echo "Two parameters must be provided to this script:"
    echo "  1. input folder [a folder containing differences (json) files"
    echo "     within sub-directories as produced by e.g. the script"
    echo "     ./DockerExtractBuildingDates.sh],"
    echo "  2. the output folder holding the computed tileset."
    echo "Note: the rest i.e. almost everything is alas hardwired."
    exit 1
fi

# Note: if you wonder where the configuration files of the form
# CityTilerDBConfigYYYY.yml (that end up in ../Docker/CityTiler-DockerContext/)
# might come from then look in the configuration section of
# ComputeLyonCityEvolution.sh

pushd ../Docker/
docker build -t liris:Py3dTilesTiler CityTiler-DockerContext
popd

run_docker() {
  # We must by-pass the entry-point and invoke a shell by hand in 
  # order to avoid to get bitten by some premature shell interpretation
  # of the wildcard argument of the --temporal_graph flag (references:
  #  - https://stackoverflow.com/questions/41428013/why-does-wildcard-for-jar-execution-not-work-in-docker-cmd
  #  - https://github.com/moby/moby/issues/12558):
  docker run \
    --mount src=`pwd`/$1,target=/Input,type=bind \
    --mount src=`pwd`/$2,target=/Output,type=bind \
    --entrypoint /bin/bash \
    -t liris:Py3dTilesTiler \
    -c 'python Tilers/CityTiler/CityTemporalTiler.py \
    --db_config_path Tilers/CityTiler/CityTilerDBConfig2009.yml \
                     Tilers/CityTiler/CityTilerDBConfig2012.yml \
                     Tilers/CityTiler/CityTilerDBConfig2015.yml \
    --time_stamp 2009 2012 2015                                 \
    --temporal_graph /Input/*DifferencesAsGraph.json \
    && \
    cp -r junk/tiles /Output && cp -r junk/tileset.json /Output'
  # TODO: fix that default junk output name within CityTemporalTiler.py
}

mkdir -p $2
# A single run gathers it all in a single Temporal tileset:
run_docker $1 $2
