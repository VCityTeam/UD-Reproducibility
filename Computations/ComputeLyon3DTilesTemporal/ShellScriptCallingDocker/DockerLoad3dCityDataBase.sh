# !/bin/sh
# set -ex

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# Note: in the following ImpExp is a short for 3dCityDB-Importer-Exporter

# Check that parameters are correctly provided
if [ $# != 3 ]
  then
	  echo "Two parameters must be provided to this script:"
    echo "  1. the (3dCity) database name where files should be imported,"
    echo "  2. pathname (absolute or relative) of the input folder holding the ImpExp"
    echo "     configuration file."
    echo "  3. pathname (absolute or relative) of input folder (a folder containing"
    echo "     the CityGML data of all the boroughs of the city of Lyon for a given"
    echo "     year like the one produced by the script DockerDownloadPatchLyonCityGML.sh), "
    exit 1
fi

realpath() {
  # https://stackoverflow.com/questions/4175264/bash-retrieve-absolute-path-given-relative
  # Returns the absolute path of the relative path given in argument
  echo "$(cd "$(dirname "$1")"; pwd)/$(basename "$1")"
}

# Instructions on using the 3DCitydb-Importer_Exporter within docker are given by
# https://github.com/tum-gis/3dcitydb-importer-exporter-docker
# as pointed by https://github.com/3dcitydb/importer-exporter/issues/99
git clone https://github.com/tum-gis/3dcitydb-importer-exporter-docker
impexp_version='4.2.2'
docker build -t tumgis/3dcitydb-impexp:${impexp_version} 3dcitydb-importer-exporter-docker/

run_docker() {
  InputConfigAbsFilename=$(realpath ${1})
  InputConfigAbsDir=$(dirname ${InputConfigAbsFilename})
  InputConfigFilename=$(basename ${InputConfigAbsFilename})
  InputFilesAbsDir=$(realpath ${2})
  docker run --name 3dcitydb-impexp \
    --mount src=${InputConfigAbsDir},target=/InputConfig,type=bind \
    --mount src=${InputFilesAbsDir},target=/InputFiles,type=bind \
    tumgis/3dcitydb-impexp:4.2.2 \
    -config /InputConfig/${InputConfigFilename} \
    -import /InputFiles/*.gml
  docker rm 3dcitydb-impexp
}

run_docker ${2} ${3}
