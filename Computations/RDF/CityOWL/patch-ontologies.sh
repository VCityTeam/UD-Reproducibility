#!/bin/sh

cp stage-1/ACMAPPER/*/* ./stage-2
echo "patching appearance.ttl.."
python3 ontologyPatcher.py ./stage-1/appearance.ttl ./stage-2/appearance.ttl
echo "patching bridge.ttl.."
python3 ontologyPatcher.py ./stage-1/bridge.ttl ./stage-2/bridge.ttl
echo "patching building.ttl.."
python3 ontologyPatcher.py ./stage-1/building.ttl ./stage-2/building.ttl
echo "patching cityfurniture.ttl.."
python3 ontologyPatcher.py ./stage-1/cityfurniture.ttl ./stage-2/cityfurniture.ttl
echo "patching cityobjectgroup.ttl.."
python3 ontologyPatcher.py ./stage-1/cityobjectgroup.ttl ./stage-2/cityobjectgroup.ttl
echo "patching construction.ttl.."
python3 ontologyPatcher.py ./stage-1/construction.ttl ./stage-2/construction.ttl
echo "patching core.ttl.."
python3 ontologyPatcher.py ./stage-1/core.ttl ./stage-2/core.ttl
echo "patching document.ttl.."
python3 ontologyPatcher.py ./stage-1/document.ttl ./stage-2/document.ttl
echo "patching dynamizer.ttl.."
python3 ontologyPatcher.py ./stage-1/dynamizer.ttl ./stage-2/dynamizer.ttl
echo "patching generics.ttl.."
python3 ontologyPatcher.py ./stage-1/generics.ttl ./stage-2/generics.ttl
echo "patching landuse.ttl.."
python3 ontologyPatcher.py ./stage-1/landuse.ttl ./stage-2/landuse.ttl
echo "patching pointcloud.ttl.."
python3 ontologyPatcher.py ./stage-1/pointcloud.ttl ./stage-2/pointcloud.ttl
echo "patching relief.ttl.."
python3 ontologyPatcher.py ./stage-1/relief.ttl ./stage-2/relief.ttl
echo "patching transportation.ttl.."
python3 ontologyPatcher.py ./stage-1/transportation.ttl ./stage-2/transportation.ttl
echo "patching tunnel.ttl.."
python3 ontologyPatcher.py ./stage-1/tunnel.ttl ./stage-2/tunnel.ttl
echo "patching vegetation.ttl.."
python3 ontologyPatcher.py ./stage-1/vegetation.ttl ./stage-2/vegetation.ttl
echo "patching versioning.ttl.."
python3 ontologyPatcher.py ./stage-1/versioning.ttl ./stage-2/versioning.ttl
echo "patching waterbody.ttl.."
python3 ontologyPatcher.py ./stage-1/waterbody.ttl ./stage-2/waterbody.ttl
echo "patching workspace.ttl.."
python3 ontologyPatcher.py ./stage-1/workspace.ttl ./stage-2/workspace.ttl
