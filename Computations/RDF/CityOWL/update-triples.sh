# #!/bin/sh

if test ! -d ./output; then
    mkdir ./output
fi

# ### Add codeList concept schemes
echo 'Adding bridge-codes.ttl'
python3 add_triples.py ./stage-2/bridge.ttl ./additional-triples/bridge-codes.ttl ./output/bridge.ttl
echo 'Adding building-codes.ttl'
python3 add_triples.py ./stage-2/building.ttl ./additional-triples/building-codes.ttl ./output/building.ttl
echo 'Adding construction-codes.ttl'
python3 add_triples.py ./stage-2/construction.ttl ./additional-triples/construction-codes.ttl ./output/construction.ttl
echo 'Adding core-codes.ttl'
python3 add_triples.py ./stage-2/core.ttl ./additional-triples/core-codes.ttl ./output/core.ttl
echo 'Adding document-codes.ttl'
python3 add_triples.py ./stage-2/document.ttl ./additional-triples/document-codes.ttl ./output/document.ttl
echo 'Adding dynamizer-codes.ttl'
python3 add_triples.py ./stage-2/dynamizer.ttl ./additional-triples/dynamizer-codes.ttl ./output/dynamizer.ttl
echo 'Adding furniture-codes.ttl'
python3 add_triples.py ./stage-2/cityfurniture.ttl ./additional-triples/furniture-codes.ttl ./output/cityfurniture.ttl
echo 'Adding generics-codes.ttl'
python3 add_triples.py ./stage-2/generics.ttl ./additional-triples/generics-codes.ttl ./output/generics.ttl
echo 'Adding group-codes.ttl'
python3 add_triples.py ./stage-2/cityobjectgroup.ttl ./additional-triples/group-codes.ttl ./output/cityobjectgroup.ttl
echo 'Adding landuse-codes.ttl'
python3 add_triples.py ./stage-2/landuse.ttl ./additional-triples/landuse-codes.ttl ./output/landuse.ttl
echo 'Adding transportation-codes.ttl'
python3 add_triples.py ./stage-2/transportation.ttl ./additional-triples/transportation-codes.ttl ./output/transportation.ttl
echo 'Adding tunnel-codes.ttl'
python3 add_triples.py ./stage-2/tunnel.ttl ./additional-triples/tunnel-codes.ttl ./output/tunnel.ttl
echo 'Adding vegetation-codes.ttl'
python3 add_triples.py ./stage-2/vegetation.ttl ./additional-triples/vegetation-codes.ttl ./output/vegetation.ttl
echo 'Adding waterbody-codes.ttl'
python3 add_triples.py ./stage-2/waterbody.ttl ./additional-triples/waterbody-codes.ttl ./output/waterbody.ttl

# ### Additional modification ###
echo 'Adding cityModelMember modifications'
python3 add_triples.py ./output/core.ttl ./additional-triples/citymodelmember.ttl ./output/core.ttl
echo 'Adding GeoSPARQL and OWL-Time alignments'
python3 add_triples.py ./output/core.ttl ./additional-triples/alignments.ttl ./output/core.ttl
echo 'Removing outdated core triples'
python3 update_graph.py ./output/core.ttl ./output/core.ttl \
   'PREFIX owl:  <http://www.w3.org/2002/07/owl#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd:  <http://www.w3.org/2001/XMLSchema#>
    PREFIX core: <https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Ontologies/CityGML/3.0/core#>

    DELETE DATA {
        core:AbstractFeatureWithLifespan.validFrom a owl:DatatypeProperty ;
            rdfs:range xsd:dateTime .
        core:AbstractFeatureWithLifespan.validTo a owl:DatatypeProperty ;
            rdfs:range xsd:dateTime .
        core:AbstractFeatureWithLifespan.creationDate a owl:DatatypeProperty ;
            rdfs:range xsd:dateTime .
        core:AbstractFeatureWithLifespan.terminationDate a owl:DatatypeProperty ;
            rdfs:range xsd:dateTime .
    }'
echo 'Removing outdated versioning triples'
python3 update_graph.py ./output/versioning.ttl ./output/versioning.ttl \
'PREFIX owl:  <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX vers: <https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Ontologies/CityGML/3.0/versioning#>

DELETE DATA {
    vers:TransactionTypeValue a rdfs:Datatype .
} ;
INSERT DATA {
    vers:TransactionTypeValue a owl:Class ;
        rdfs:subClassOf skos:Concept .
}'


### Copy remaining files ###
for file in ./stage-2/*
do 
    file_name=$(basename "$file")
    if test ! -f "./output/$file_name" ; then
        echo "Copying $file to ./output/$file_name"
        cp $file ./output/$file_name
    fi
done

echo 'Copying CityOWL.ttl to output'
cp ./additional-triples/CityOWL.ttl ./output
echo 'Copying transactiontypevalues.ttl to output'
cp ./additional-triples/transactiontypevalues.ttl ./output