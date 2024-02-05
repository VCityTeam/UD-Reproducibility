#!/bin/sh

mkdir ./stage-3
echo "Adding bridge-codes.ttl"
python3 add_triples.py ./stage-2/bridge.ttl ./concept-schemes/bridge-codes.ttl ./stage-3/bridge.ttl
echo "Adding building-codes.ttl"
python3 add_triples.py ./stage-2/building.ttl ./concept-schemes/building-codes.ttl ./stage-3/building.ttl
echo "Adding construction-codes.ttl"
python3 add_triples.py ./stage-2/construction.ttl ./concept-schemes/construction-codes.ttl ./stage-3/construction.ttl
echo "Adding core-codes.ttl"
python3 add_triples.py ./stage-2/core.ttl ./concept-schemes/core-codes.ttl ./stage-3/core.ttl
echo "Adding document-codes.ttl"
python3 add_triples.py ./stage-2/document.ttl ./concept-schemes/document-codes.ttl ./stage-3/document.ttl
echo "Adding dynamizer-codes.ttl"
python3 add_triples.py ./stage-2/dynamizer.ttl ./concept-schemes/dynamizer-codes.ttl ./stage-3/dynamizer.ttl
echo "Adding furniture-codes.ttl"
python3 add_triples.py ./stage-2/cityfurniture.ttl ./concept-schemes/furniture-codes.ttl ./stage-3/cityfurniture.ttl
echo "Adding generics-codes.ttl"
python3 add_triples.py ./stage-2/generics.ttl ./concept-schemes/generics-codes.ttl ./stage-3/generics.ttl
echo "Adding group-codes.ttl"
python3 add_triples.py ./stage-2/cityobjectgroup.ttl ./concept-schemes/group-codes.ttl ./stage-3/cityobjectgroup.ttl
echo "Adding landuse-codes.ttl"
python3 add_triples.py ./stage-2/landuse.ttl ./concept-schemes/landuse-codes.ttl ./stage-3/landuse.ttl
echo "Adding transportation-codes.ttl"
python3 add_triples.py ./stage-2/transportation.ttl ./concept-schemes/transportation-codes.ttl ./stage-3/transportation.ttl
echo "Adding tunnel-codes.ttl"
python3 add_triples.py ./stage-2/tunnel.ttl ./concept-schemes/tunnel-codes.ttl ./stage-3/tunnel.ttl
echo "Adding vegetation-codes.ttl"
python3 add_triples.py ./stage-2/vegetation.ttl ./concept-schemes/vegetation-codes.ttl ./stage-3/vegetation.ttl
echo "Adding waterbody-codes.ttl"
python3 add_triples.py ./stage-2/waterbody.ttl ./concept-schemes/waterbody-codes.ttl ./stage-3/waterbody.ttl
