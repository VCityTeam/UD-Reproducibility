#!/bin/sh

cp ./stage-2/* ./stage-3/
echo "Adding bridge-codes.ttl"
python3 add_triples.py ./input/bridge.ttl ./concept-schemes/bridge-codes.ttl ./input/bridge.ttl
echo "Adding building-codes.ttl"
python3 add_triples.py ./input/building.ttl ./concept-schemes/building-codes.ttl ./input/building.ttl
echo "Adding construction-codes.ttl"
python3 add_triples.py ./input/construction.ttl ./concept-schemes/construction-codes.ttl ./input/construction.ttl
echo "Adding core-codes.ttl"
python3 add_triples.py ./input/core.ttl ./concept-schemes/core-codes.ttl ./input/core.ttl
echo "Adding document-codes.ttl"
python3 add_triples.py ./input/document.ttl ./concept-schemes/document-codes.ttl ./input/document.ttl
echo "Adding dynamizer-codes.ttl"
python3 add_triples.py ./input/dynamizer.ttl ./concept-schemes/dynamizer-codes.ttl ./input/dynamizer.ttl
echo "Adding furniture-codes.ttl"
python3 add_triples.py ./input/cityfurniture.ttl ./concept-schemes/furniture-codes.ttl ./input/cityfurniture.ttl
echo "Adding generics-codes.ttl"
python3 add_triples.py ./input/generics.ttl ./concept-schemes/generics-codes.ttl ./input/generics.ttl
echo "Adding group-codes.ttl"
python3 add_triples.py ./input/cityobjectgroup.ttl ./concept-schemes/group-codes.ttl ./input/cityobjectgroup.ttl
echo "Adding landuse-codes.ttl"
python3 add_triples.py ./input/landuse.ttl ./concept-schemes/landuse-codes.ttl ./input/landuse.ttl
echo "Adding transportation-codes.ttl"
python3 add_triples.py ./input/transportation.ttl ./concept-schemes/transportation-codes.ttl ./input/transportation.ttl
echo "Adding tunnel-codes.ttl"
python3 add_triples.py ./input/tunnel.ttl ./concept-schemes/tunnel-codes.ttl ./input/tunnel.ttl
echo "Adding vegetation-codes.ttl"
python3 add_triples.py ./input/vegetation.ttl ./concept-schemes/vegetation-codes.ttl ./input/vegetation.ttl
echo "Adding waterbody-codes.ttl"
python3 add_triples.py ./input/waterbody.ttl ./concept-schemes/waterbody-codes.ttl ./input/waterbody.ttl
