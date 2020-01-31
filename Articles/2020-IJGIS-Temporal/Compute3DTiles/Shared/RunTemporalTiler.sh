# !/bin/sh

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit


if [ $# != 5 ]; then
    echo "Two parameters must be provided to this script:"
    echo "  1. the output folder holding the computed tileset."
    echo "  2. the first database server configuration file."
    echo "  3. the second database server configuration file."
    echo "  4. the third database server configuration file."
    echo "  5. the input folder [a folder containing differences (json) files"
    echo "     within sub-directories as produced by e.g. the script"
    echo "     ./DockerExtractBuildingDates.sh],"
    echo "Note: the rest i.e. almost everything is alas hardwired."
    exit 1
fi

# Note: if you wonder where the configuration files of the form
# CityTilerDBConfigYYYY.yml (that end up in Docker/CityTiler-DockerContext/)
# might come from then look in the configuration section of the script
# invoking this one.

pushd Docker/
docker build -t liris:Py3dTilesTiler CityTiler-DockerContext
popd

run_docker() {
  docker run \
    --mount src=`pwd`/$1,target=/Output,type=bind \
    --mount src=`pwd`/$5,target=/Input,type=bind \
    -t liris:Py3dTilesTiler \
    TemporalTiler \
    --db_config_path $2 $3 $4 \
    --time_stamp 2009 2012 2015
  # Because we want to aboid globing `pwd`/$2=/Input directory (in order to
  # retrieve all the difference graph designated by a wildcarded expression
  # of the form /Input/*DifferencesAsGraph.json that would be interpreted by
  # the present invocation shell as opposed to the entrypoint context), the
  # following argument (transposed logical equivalents) is hardwired in
  # the entrypoint.py
  #   --temporal_graph /Input/*DifferencesAsGraph.json
}

mkdir -p $1
# A single run gathers it all in a single Temporal tileset:
run_docker $1 $2 $3 $4 $5
