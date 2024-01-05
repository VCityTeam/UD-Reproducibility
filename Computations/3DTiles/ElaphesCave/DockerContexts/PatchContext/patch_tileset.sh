#!/bin/bash
# $1: the directory holding the 3DTiles directory to be patched

# Check argument directory exists
if [ ! -d ${1} ]
then
  echo "Unfound (argument) ${1} directory."
  echo "Maybe the mountpoint (provided with e.g. with -v `pwd`:/data as docker argument) is missing/erroneous?."
  echo "Exiting"
  exit 1
fi

# Expected existing 3DTiles
if [ ! -f ${1}/tileset.json ]
then
  echo "Unfound expected ${1}/tileset.json file)."
  echo "Exiting"
  exit 1
fi
cd ${1}

# Create a new tileset entrypoint by applying the patch.
# The patch was (brutally) embarked in the container at build time
cp tileset.json tileset.json.orig
patch tileset.json /Exp-Cloud-ELAPHS-94M-3DTiles-Lyon.patch
mv tileset.json tileset-lyon_offset.json
mv tileset.json.orig tileset.json
