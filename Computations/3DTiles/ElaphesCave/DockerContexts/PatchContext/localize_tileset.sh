#!/bin/bash
# $1: the directory holding the 3DTiles directory to be patched

# Check argument directory exists
if [ ! -f ${1} ]
then
  echo "Unfound (argument) file ${1}."
  echo "A tileset.json argument filename was expected."
  echo "Maybe the mountpoint (provided with e.g. with -v `pwd`:/data as docker argument) is missing/erroneous?."
  echo "Exiting"
  exit 1
fi

# Create a new tileset entrypoint by applying the patch.
# The patch was (brutally) embarked in the container at build time
TARGET=$(dirname "${1}")/tileset-lyon_offset.json
sed -e 's/\"transform\": \[1\.0, 0\.0, 0\.0, 0\.0, 0\.0, 1\.0, 0\.0, 0\.0, 0\.0, 0\.0, 1\.0, 0\.0, -9\.939101524517511, -3\.2372710606817234, -6\.963341127647212, 1\.0\]/\"transform\": \[1\.0, 0\.0, 0\.0, 0\.0, 0\.0, 1\.0, 0\.0, 0\.0, 0\.0, 0\.0, 1\.0, 0\.0, 1841761\.4663378098, 5175204\.0252315905, 300\.1, 1\.0\]/' ${1} > ${TARGET}

