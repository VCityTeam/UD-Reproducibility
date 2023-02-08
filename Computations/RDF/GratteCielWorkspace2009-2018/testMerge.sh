#!/bin/sh

python add_triples.py \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2009_split.ttl \
    ../DifferenceGraph-to-CityGML3/GratteCiel_2009_split.ttl \
    GratteCiel_2009_split.ttl

python add_triples.py \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2012_split.ttl \
    ../DifferenceGraph-to-CityGML3/GratteCiel_2012_split.ttl \
    GratteCiel_2012_split.ttl

python add_triples.py \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2015_split.ttl \
    ../DifferenceGraph-to-CityGML3/GratteCiel_2015_split.ttl \
    GratteCiel_2015_split.ttl

python add_triples.py \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2018_split.ttl \
    ../DifferenceGraph-to-CityGML3/GratteCiel_2018_split.ttl \
    GratteCiel_2018_split.ttl

python add_triples.py \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2009_alt_split.ttl \
    ../DifferenceGraph-to-CityGML3/GratteCiel_2009_alt_split.ttl \
    GratteCiel_2009_alt_split.ttl

python add_triples.py \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2012_alt_split.ttl \
    ../DifferenceGraph-to-CityGML3/GratteCiel_2012_alt_split.ttl \
    GratteCiel_2012_alt_split.ttl