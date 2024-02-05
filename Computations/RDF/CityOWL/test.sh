#!/bin/sh

echo "Start"
python3 ontologyPatcher.py ./testlite/appearance.ttl appearance.ttl 
python3 ontologyPatcher.py ./testlite/bridge.ttl bridge.ttl 
python3 ontologyPatcher.py ./testlite/building.ttl building.ttl 
python3 ontologyPatcher.py ./testlite/cityfurniture.ttl cityfurniture.ttl 
python3 ontologyPatcher.py ./testlite/cityobjectgroup.ttl cityobjectgroup.ttl 
python3 ontologyPatcher.py ./testlite/construction.ttl construction.ttl 
python3 ontologyPatcher.py ./testlite/core.ttl core.ttl 
python3 ontologyPatcher.py ./testlite/document.ttl document.ttl 
python3 ontologyPatcher.py ./testlite/dynamizer.ttl dynamizer.ttl 
python3 ontologyPatcher.py ./testlite/generics.ttl generics.ttl 
python3 ontologyPatcher.py ./testlite/landuse.ttl landuse.ttl 
python3 ontologyPatcher.py ./testlite/pointcloud.ttl pointcloud.ttl 
python3 ontologyPatcher.py ./testlite/relief.ttl relief.ttl 
python3 ontologyPatcher.py ./testlite/transportation.ttl transportation.ttl 
python3 ontologyPatcher.py ./testlite/tunnel.ttl tunnel.ttl 
python3 ontologyPatcher.py ./testlite/vegetation.ttl vegetation.ttl 
python3 ontologyPatcher.py ./testlite/versioning.ttl versioning.ttl 
python3 ontologyPatcher.py ./testlite/waterbody.ttl waterbody.ttl 
python3 ontologyPatcher.py ./testlite/workspace.ttl workspace.ttl
echo "End"