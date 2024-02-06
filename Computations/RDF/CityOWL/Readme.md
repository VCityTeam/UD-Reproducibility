# How to generate CityOWL

CityOWL is an OWL/RDF representation of the CityGML 3.0 Conceptual Model (CM). This folder contains instructions for how to generate CityOWL and two experimental CityGML extensions (or ADEs). Two CityGML transformations are proposed:

- CityOWL CWA (Closed World Assumption) - Much more constrained and expressive
- CityOWL OWA (Open World Assumption) - Much less constrained. Only contains classes, properties, and datatypes. Properties only contain `rdfs:domain` and `rdfs:range` declarations.

- [How to generate CityOWL](#how-to-generate-cityowl)
  - [Dependencies](#dependencies)
  - [Instructions](#instructions)

## Dependencies

- [ShapeChange](https://shapechange.github.io/ShapeChange/3.0.0/get%20started/Get_Started.html) v3.0.0
  - These instructions assume the ShapeChange jar (and its dependencies) are stored in this directory. 
- UD-Graph scripts:
  - Requires [Python3](https://www.python.org/downloads/)
  - To download:
      ```bash
      git clone https://github.com/VCityTeam/UD-Graph.git
      cd UD-Graph
      checkout 354fddb
      ```
  - Move the [ontology patcher](https://github.com/VCityTeam/UD-Graph/tree/master/Transformations/ShapeChange#to-run-the-ontology-patcher) script to the same folder as this readme
      ```bash
      cp ./UD-Graph/Transformations/ShapeChange/ontologyPatcher.py [path to this directory]
      ```
  - Download [addTriples](https://github.com/VCityTeam/UD-Graph/tree/master/Transformations/utilities#add_triplespy) script to the same folder as this readme
      ```bash
      cp ./UD-Graph/Transformations/utilities/add_triples.py [path to this directory]
      ```

## Instructions
Run the entire workflow using recommended inputs and configurations:
```bash
./run-workflow.sh
```
- Note: run `./clean.sh` to remove workflow results if you need

To run each stage, follow these step:
1. Setup a staging folder, `input`, to get started:
   ```bash
   mkdir input
   ```
2. Download one (or both) of the CityGML 3.0 CMs (with the Document and Workspace ADEs) [from UD-Graph](https://github.com/VCityTeam/UD-Graph/tree/a012111a935e0dd8eb9d661fbbfb4110e55561d0/Transformations/test-data/UML):
   - `CityGML_3.0-workspaces-documents_shapechange-export.xml` (Recommended) - An optimized ShapeChange UML format. Produces much faster ShapeChange transformations.
      ```bash
      cp ./UD-Graph/Transformations/test-data/UML/CityGML_3.0-workspaces-documents_shapechange-export.xml ./input
      ```
   - `CityGML_3.0-workspaces-documents.eap` - Enterprise Architect (EA) format. Transformation requires Windows and following the [ShapeChange installation instructions](#dependencies) for enabeling Enterprise Architect models.
      ```bash
      cp ./UD-Graph/Transformations/test-data/UML/CityGML_3.0-workspaces-documents.eap ./input
      ```
3. Choose one (or both) of the following ShapeChange configuration files based on your needs:
   - For CityOWL OWA: [./shapechange-configs/CityGML3.0_to_OWL_lite_config.xml](./shapechange-configs/CityGML3.0_to_OWL_lite_config.xml)
   - For CityOWL CWA: [./shapechange-configs/CityGML3.0_to_OWL_config.xml](./shapechange-configs/CityGML3.0_to_OWL_config.xml)
   - If using a EA format for step 2, comment line 4 and uncomment line 3 in the selected config.
      ```xml
      <parameter name="inputModelType" value="EA7"/>
      <!-- <parameter name="inputModelType" value="SCXML"/> -->
      ```
4. Transform with ShapeChange. For example, to transform using the OWA configuration:
      ```bash
      java -jar ./ShapeChange-3.0.0.jar -Dfile.encoding=UTF-8 \
         -c ./shapechange-configs/CityGML3.0_to_OWL_lite_config.xml \
         -x '$input$' './input/CityGML_3.0-workspaces-documents_shapechange-export.xml' \
         -x '$output$' 'stage-1'
      ```
5. Next we must patch and modify the generated ontologies. Run the UD-Graph ontology patcher on each generated ontology:
      ```bash
      ./patch-ontologies.sh
      ```
   -  This script also fixes the URIs of the Document and Workspace ADEs.
6. Add CodeLists, CityModelMember modifications, and proposed alignments between CityGML, GeoSPARQL, and OWL-Time. Currently, the shapechange rule to generate codelists automatically as SKOS concept schemes does not work with the CityGML CM. These have been created manually as an external files and must be added to each ontology. Run the UD-Graph add_triples and update_rdf scripts on each generated ontology:
   ```bash
   ./update-triples.sh
   ```
7.   (Optional) test with [Protégé](https://protege.stanford.edu/software.php#desktop-protege) that the ontologies load.
   1. Test with and without importing external ontologies online.
   2. Test ontologies are logically sound with a reasoner.
