#!/bin/sh

if test ! -d ./stage-2; then
    mkdir ./stage-2
fi

echo "patching appearance.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/appearance/appearance.ttl ./stage-2/appearance.ttl
echo "patching bridge.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/bridge/bridge.ttl ./stage-2/bridge.ttl
echo "patching building.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/building/building.ttl ./stage-2/building.ttl
echo "patching cityfurniture.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/cityfurniture/cityfurniture.ttl ./stage-2/cityfurniture.ttl
echo "patching cityobjectgroup.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/cityobjectgroup/cityobjectgroup.ttl ./stage-2/cityobjectgroup.ttl
echo "patching construction.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/construction/construction.ttl ./stage-2/construction.ttl
echo "patching core.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/core/core.ttl ./stage-2/core.ttl
echo "patching document.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/document/document.ttl ./stage-2/document.ttl
echo "patching dynamizer.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/dynamizer/dynamizer.ttl ./stage-2/dynamizer.ttl
echo "patching generics.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/generics/generics.ttl ./stage-2/generics.ttl
echo "patching landuse.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/landuse/landuse.ttl ./stage-2/landuse.ttl
echo "patching pointcloud.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/pointcloud/pointcloud.ttl ./stage-2/pointcloud.ttl
echo "patching relief.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/relief/relief.ttl ./stage-2/relief.ttl
echo "patching transportation.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/transportation/transportation.ttl ./stage-2/transportation.ttl
echo "patching tunnel.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/tunnel/tunnel.ttl ./stage-2/tunnel.ttl
echo "patching vegetation.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/vegetation/vegetation.ttl ./stage-2/vegetation.ttl
echo "patching versioning.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/versioning/versioning.ttl ./stage-2/versioning.ttl
echo "patching waterbody.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/waterbody/waterbody.ttl ./stage-2/waterbody.ttl
echo "patching workspace.ttl"
python3 ontologyPatcher.py ./stage-1/FLATTENER1/workspace/workspace.ttl ./stage-2/workspace.ttl

echo 'updating ADE URIs'
cat ./stage-2/document.ttl | sed 's/\/CityGML\/3\.0\/document/\/Document\/3\.0\/document/g' > ./stage-2/document.tmp
mv ./stage-2/document.tmp ./stage-2/document.ttl # not sure why this is necessary but it works on my machine
cat ./stage-2/workspace.ttl | sed 's/\/CityGML\/3\.0\/workspace/\/Workspace\/3\.0\/workspace/g' > ./stage-2/workspace.tmp
mv ./stage-2/workspace.tmp ./stage-2/workspace.ttl # not sure why this is necessary but it works on my machine
