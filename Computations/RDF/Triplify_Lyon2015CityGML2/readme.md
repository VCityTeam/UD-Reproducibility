## Pre-requisites
 - [install docker](https://docs.docker.com/engine/install/)
 - [install Python3.8](https://www.python.org/)
 - virtualenv:
```
pip install virtualenv 
```

## Installing dependencies

Create a python virtual environment and activate it

```bash
$ virtualenv -p python venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```

## Running the triplifier workflow

From the same python virtual environment run the workflow

```bash
(venv)$ python run_citygml2_lyon_workflow.py
```

Note that the workflow configuration can be customized in `./demo_setup_citygml2_lyon_workflow.py`

## Whats being executed
### UML to OWL transformation with ShapeChange
We propose using ShapeChange for transforming the CityGML UML model to OWL/RDF.
These instructions are written with ShapeChange version 2.11.0.
To execute this transformation, first [download and unpack ShapeChange](https://shapechange.net/get-started/) and place the ShapeChange JAR file in the `./lib` directory.

1. Transform UML models in the proprietary Enterprise Architect format `.eap` to the ShapeChange specific XML format. This can speed up transformations and is helpful when testing different ShapeChange configurations.
   -  ```bash
      # for the CityGML 2.0 model 
      java -jar ./lib/ShapeChange-2.11.0.jar -Dfile.encoding=UTF-8 -c CityGML2.0_config.xml \
      -x '$input$' './test-data/UML/CityGML_2.0_versioning_workspace_document.xml' \
      -x '$output$' './test-data/UML/'

      # for the CityGML 3.0 model 
      java -jar ./lib/ShapeChange-2.11.0.jar -Dfile.encoding=UTF-8 -c CityGML3.0_config.xml \
      -x '$input$' './test-data/UML/CityGML_3.0_versioning_workspace_document.xml' \
      -x '$output$' './test-data/UML/'
      ```
      - The output of these tranformations are located [here](./test-data/UML/)
2. Transform the models using [this configuration file](./ShapeChange/CityGML2.0_to_OWL_config.xml) and [these custom mappings](./ShapeChange/StandardMapEntries_iso19107-owl.xml).
   -  ```bash
      # for the CityGML 2.0 model
      java -jar ./lib/ShapeChange-2.11.0.jar -Dfile.encoding=UTF-8 -c CityGML2.0_config.xml \
      -x '$input$' './test-data/UML/CityGML_2.0_versioning_workspace_document_shapechange-export.xml' \
      -x '$output$' './test-data/OWL/CityGML_2.0_Conceptual_Model' \
      -x '$localdir$' './ShapeChange'

      # for the CityGML 3.0 model
      java -jar ./lib/ShapeChange-2.11.0.jar -Dfile.encoding=UTF-8 -c CityGML3.0_config.xml \
      -x '$input$' './test-data/UML/CityGML_3.0-workspaces-documents_shapechange-export.xml' \
      -x '$output$' './test-data/OWL/CityGML_3.0_Conceptual_Model' \
      -x '$localdir$' './ShapeChange'
      ```
   - This will produce the CityGML networks of ontologies [here](./test-data/OWL/) (one ontology per CityGML module)
3. As of version 2.11.0 of ShapeChange, theses configurations produce ontologies in the OWL-Full OWL sublanguage. This sublanguage is not [decidable](https://en.wikipedia.org/wiki/Decidability_(logic)). To "patch" generated ontologies to the decidable OWL-DL sublanguage, use the [ontologyPatcher.py script](./XML-to-RDF/ontologyPatcher.py). This step is technically optional but recommended if the generated ontologies will be used for reasoning:
   -  ```bash
      mkdir ./3.0
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/appearance/appearance.ttl ./3.0/appearance.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/bridge/bridge.ttl ./3.0/bridge.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/building/building.ttl ./3.0/building.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/cityfurniture/cityfurniture.ttl ./3.0/cityfurniture.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/cityobjectgroup/cityobjectgroup.ttl ./3.0/cityobjectgroup.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/construction/construction.ttl ./3.0/construction.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/core/core.ttl ./3.0/core.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/dynamizer/dynamizer.ttl ./3.0/dynamizer.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/generics/generics.ttl ./3.0/generics.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/landuse/landuse.ttl ./3.0/landuse.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/pointcloud/pointcloud.ttl ./3.0/pointcloud.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/relief/relief.ttl ./3.0/relief.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/transportation/transportation.ttl ./3.0/transportation.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/tunnel/tunnel.ttl ./3.0/tunnel.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/vegetation/vegetation.ttl ./3.0/vegetation.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/versioning/versioning.ttl ./3.0/versioning.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/waterbody/waterbody.ttl ./3.0/waterbody.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/document/document.ttl ./3.0/document.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_3.0_Conceptual_Model/FLATTENER1/workspace/workspace.ttl ./3.0/workspace.ttl
      ```
      To transform the CityGML 2.0 ontologies generated using the `CityGML2.0_to_OWL_config.xml` configuration the following can be used:
      ```bash
      mkdir ./2.0
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/core/core.ttl ./2.0/core.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/appearance/appearance.ttl ./2.0/appearance.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/bridge/bridge.ttl ./2.0/bridge.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/building/building.ttl ./2.0/building.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/cityfurniture/cityfurniture.ttl ./2.0/cityfurniture.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/cityobjectgroup/cityobjectgroup.ttl ./2.0/cityobjectgroup.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/core/core.ttl ./2.0/core.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/generics/generics.ttl ./2.0/generics.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/landuse/landuse.ttl ./2.0/landuse.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/relief/relief.ttl ./2.0/relief.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/transportation/transportation.ttl ./2.0/transportation.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/tunnel/tunnel.ttl ./2.0/tunnel.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/vegetation/vegetation.ttl ./2.0/vegetation.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/waterbody/waterbody.ttl ./2.0/waterbody.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/document/document.ttl ./2.0/document.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/version/version.ttl ./2.0/version.ttl
      python ontologyPatcher.py ../test-data/OWL/CityGML_2.0_Conceptual_Model/FLATTENER1/workspace/workspace.ttl ./2.0/workspace.ttl
      ```
### XML to OWL transformation with XML2RDF.py
1. Transform the [CityGML XML data](./test-data/GML/) to OWL/RDF using the generated ontology network (with the GeoSPARQL ontology) and a [namespace mapping configuration file](./XML-to-RDF/citygml_3_mappings.json). Note that the ontology network and proposed namespace mappings are supplemented by ISO 191xx ontologies for GML concepts not represented by the GeoSPARQL model
   -  ```bash
      cd ./XML-to-RDF
      # for CityGML 2.0:
      python ./XML2RDF.py \
      -v \
      --format ttl \
      ../test-data/GML/Lyon_1er_arrondisement/LYON_1ER_BATI_2015-1_bldg-patched.gml \
      ./citygml_2_mappings.json \
      ../../Ontologies/CityGML/2.0/ \
      https://www.w3.org/2009/08/skos-reference/skos.rdf \
      http://www.opengis.net/ont/geosparql# \
      http://www.opengis.net/ont/gml# \
      ../../Ontologies/Alignments \
      https://def.isotc211.org/ontologies/iso19136/2007/Feature.rdf \
      https://def.isotc211.org/ontologies/iso19107/2003/CoordinateGeometry.rdf

      # for CityGML 3.0:
      python XML2RDF.py \
      -v \
      --format ttl \
      ../test-data/GML/Building_CityGML3.0_LOD2_with_several_attributes.gml \
      citygml_3_mappings.json \
      ../../Ontologies/CityGML/3.0/ \
      https://www.w3.org/2009/08/skos-reference/skos.rdf \
      http://www.opengis.net/ont/geosparql# \
      http://www.opengis.net/ont/gml# \
      ../../Ontologies/Alignments \
      https://def.isotc211.org/ontologies/iso19136/2007/Feature.rdf \
      https://def.isotc211.org/ontologies/iso19107/2003/CoordinateGeometry.rdf
      ```