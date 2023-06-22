#!/bin/sh

python XML2RDF.py \
    -v \
    --log 2009alt.log \
    --format ttl \
    [input folder]/3.0/VILLEURBANNE_BATI_2009_alt_split.gml \
    citygml_3_mappings.json \
    ../../Ontologies/CityGML/2.0/core.ttl \
    ../../Ontologies/CityGML/2.0/appearance.ttl \
    ../../Ontologies/CityGML/2.0/building.ttl \
    ../../Ontologies/CityGML/2.0/generics.ttl \
    https://www.w3.org/2009/08/skos-reference/skos.rdf \
    http://www.opengis.net/ont/geosparql# \
    http://www.opengis.net/ont/gml# \
    ../../Ontologies/Alignments/CityGML2-ISO19136.ttl \
    ../../Ontologies/Alignments/CityGML2-GeoSPARQL.ttl \
    https://def.isotc211.org/iso19136/2007/Feature.rdf \
    https://def.isotc211.org/iso19107/2003/CoordinateGeometry.rdf 

python XML2RDF.py \
    -v \
    --log 2009.log \
    --format ttl \
    [input folder]/3.0/VILLEURBANNE_BATI_2009_split.gml \
    citygml_3_mappings.json \
    ../../Ontologies/CityGML/2.0/core.ttl \
    ../../Ontologies/CityGML/2.0/appearance.ttl \
    ../../Ontologies/CityGML/2.0/building.ttl \
    ../../Ontologies/CityGML/2.0/generics.ttl \
    https://www.w3.org/2009/08/skos-reference/skos.rdf \
    http://www.opengis.net/ont/geosparql# \
    http://www.opengis.net/ont/gml# \
    ../../Ontologies/Alignments/CityGML2-ISO19136.ttl \
    ../../Ontologies/Alignments/CityGML2-GeoSPARQL.ttl \
    https://def.isotc211.org/iso19136/2007/Feature.rdf \
    https://def.isotc211.org/iso19107/2003/CoordinateGeometry.rdf 

python XML2RDF.py \
    -v \
    --format ttl \
    --log 2012alt.log \
    [input folder]/3.0/VILLEURBANNE_BATI_2012_alt_split.gml \
    citygml_3_mappings.json \
    ../../Ontologies/CityGML/2.0/core.ttl \
    ../../Ontologies/CityGML/2.0/appearance.ttl \
    ../../Ontologies/CityGML/2.0/building.ttl \
    ../../Ontologies/CityGML/2.0/generics.ttl \
    https://www.w3.org/2009/08/skos-reference/skos.rdf \
    http://www.opengis.net/ont/geosparql# \
    http://www.opengis.net/ont/gml# \
    ../../Ontologies/Alignments/CityGML2-ISO19136.ttl \
    ../../Ontologies/Alignments/CityGML2-GeoSPARQL.ttl \
    https://def.isotc211.org/iso19136/2007/Feature.rdf \
    https://def.isotc211.org/iso19107/2003/CoordinateGeometry.rdf 

python XML2RDF.py \
    -v \
    --format ttl \
    --log 2012.log \
    [input folder]/3.0/VILLEURBANNE_BATI_2012_split.gml \
    citygml_3_mappings.json \
    ../../Ontologies/CityGML/2.0/core.ttl \
    ../../Ontologies/CityGML/2.0/appearance.ttl \
    ../../Ontologies/CityGML/2.0/building.ttl \
    ../../Ontologies/CityGML/2.0/generics.ttl \
    https://www.w3.org/2009/08/skos-reference/skos.rdf \
    http://www.opengis.net/ont/geosparql# \
    http://www.opengis.net/ont/gml# \
    ../../Ontologies/Alignments/CityGML2-ISO19136.ttl \
    ../../Ontologies/Alignments/CityGML2-GeoSPARQL.ttl \
    https://def.isotc211.org/iso19136/2007/Feature.rdf \
    https://def.isotc211.org/iso19107/2003/CoordinateGeometry.rdf 

python XML2RDF.py \
    -v \
    --format ttl \
    --log 2015.log \
    [input folder]/3.0/VILLEURBANNE_BATI_2015_split.gml \
    citygml_3_mappings.json \
    ../../Ontologies/CityGML/2.0/core.ttl \
    ../../Ontologies/CityGML/2.0/appearance.ttl \
    ../../Ontologies/CityGML/2.0/building.ttl \
    ../../Ontologies/CityGML/2.0/generics.ttl \
    https://www.w3.org/2009/08/skos-reference/skos.rdf \
    http://www.opengis.net/ont/geosparql# \
    http://www.opengis.net/ont/gml# \
    ../../Ontologies/Alignments/CityGML2-ISO19136.ttl \
    ../../Ontologies/Alignments/CityGML2-GeoSPARQL.ttl \
    https://def.isotc211.org/iso19136/2007/Feature.rdf \
    https://def.isotc211.org/iso19107/2003/CoordinateGeometry.rdf 

python XML2RDF.py \
    -v \
    --format ttl \
    --log 2018.log \
    [input folder]/3.0/VILLEURBANNE_BATI_2018_split.gml \
    citygml_3_mappings.json \
    ../../Ontologies/CityGML/2.0/core.ttl \
    ../../Ontologies/CityGML/2.0/appearance.ttl \
    ../../Ontologies/CityGML/2.0/building.ttl \
    ../../Ontologies/CityGML/2.0/generics.ttl \
    https://www.w3.org/2009/08/skos-reference/skos.rdf \
    http://www.opengis.net/ont/geosparql# \
    http://www.opengis.net/ont/gml# \
    ../../Ontologies/Alignments/CityGML2-ISO19136.ttl \
    ../../Ontologies/Alignments/CityGML2-GeoSPARQL.ttl \
    https://def.isotc211.org/iso19136/2007/Feature.rdf \
    https://def.isotc211.org/iso19107/2003/CoordinateGeometry.rdf 
