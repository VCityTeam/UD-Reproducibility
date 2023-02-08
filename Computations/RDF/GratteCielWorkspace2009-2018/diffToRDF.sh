#!/bin/sh

python DifferenceGraph2RDF.py \
    --base-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/Transition_2009_2012 \
    --v1-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2009_split \
    --v1-prefix v2009 \
    --v2-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2012_split \
    --v2-prefix v2012 \
    -d \
    -f ttl \
    --strip-time-stamp \
    --existence_time_stamps \
        2009-01-01T00:00:00 \
        2012-01-01T00:00:00 \
    './testGratteCiel/2009-2012-diff/DifferencesAsGraph.json' \
    2009 2012

python DifferenceGraph2RDF.py \
    --base-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/Transition_2012_2015 \
    --v1-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2012_split \
    --v1-prefix v2012 \
    --v2-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2015_split \
    --v2-prefix v2015 \
    -d \
    -f ttl \
    --strip-time-stamp \
    --existence_time_stamps \
        2012-01-01T00:00:00 \
        2015-01-01T00:00:00 \
    './testGratteCiel/2012-2015-diff/DifferencesAsGraph.json' \
    2012 2015

python DifferenceGraph2RDF.py \
    --base-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/Transition_2015_2018 \
    --v1-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2015_split \
    --v1-prefix v2015 \
    --v2-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2018_split \
    --v2-prefix v2018 \
    -d \
    -f ttl \
    --strip-time-stamp \
    --existence_time_stamps \
        2015-01-01T00:00:00 \
        2018-01-01T00:00:00 \
    './testGratteCiel/2015-2018-diff/DifferencesAsGraph.json' \
    2015 2018

python DifferenceGraph2RDF.py \
    --base-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/Transition_2009_2009b \
    --v1-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2009_split \
    --v1-prefix v2009 \
    --v2-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2009_alt_split \
    --v2-prefix v2009b \
    -d \
    -f ttl \
    --strip-time-stamp \
    --existence_time_stamps \
        2009-01-01T00:00:00 \
        2010-01-01T00:00:00 \
    './testGratteCiel/2009-2009-fork-diff/DifferencesAsGraph.json' \
    2009 2010

python DifferenceGraph2RDF.py \
    --base-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/Transition_2009b_2012b \
    --v1-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2009_alt_split \
    --v1-prefix v2009b \
    --v2-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2012_alt_split \
    --v2-prefix v2012b \
    -d \
    -f ttl \
    --strip-time-stamp \
    --existence_time_stamps \
        2009-02-01T00:00:00 \
        2012-01-01T00:00:00 \
    './testGratteCiel/2009-2012-alt-diff/DifferencesAsGraph.json' \
    2010 2013

python DifferenceGraph2RDF.py \
    --base-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/Transition_2012b_2015 \
    --v1-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2012_alt_split \
    --v1-prefix v2012b \
    --v2-uri https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2015_split \
    --v2-prefix v2015 \
    -d \
    -f ttl \
    --strip-time-stamp \
    --existence_time_stamps \
        2012-01-01T00:00:00 \
        2015-01-01T00:00:00 \
    './testGratteCiel/2012-2015-merge-diff/DifferencesAsGraph.json' \
    2013 2015