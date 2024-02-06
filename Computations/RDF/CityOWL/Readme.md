# How to generate CityOWL

CityOWL is an OWL/RDF representation of the CityGML 3.0 Conceptual Model (CM). This folder contains instructions for how to generate CityOWL and two experimental CityGML extensions (or ADEs). Two CityGML transformations are proposed:

- CityOWL CWA (Closed World Assumption) - Much more constrained and expressive
- CityOWL OWA (Open World Assumption) - Much less constrained. Only contains classes, properties, and datatypes. Properties only contain `rdfs:domain` and `rdfs:range` declarations.

- [How to generate CityOWL](#how-to-generate-cityowl)
  - [Dependencies](#dependencies)
  - [Instructions](#instructions)

## Dependencies

- [ShapeChange](https://shapechange.github.io/ShapeChange/3.0.0/get%20started/Get_Started.html) v3.0.0
- UD-Graph scripts:
  - Requires [Python3](https://www.python.org/downloads/)
  - To download:
      ```bash
      git clone https://github.com/VCityTeam/UD-Graph.git
      cd UD-Graph
      # FIXME git checkout [SHA1]
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

1. Setup a staging folder, `input`, to get started:
   ```bash
   mkdir input
   ```
2. Download one (or both) of the CityGML 3.0 CMs (with the Document and Workspace ADEs) [from UD-Graph](https://github.com/VCityTeam/UD-Graph/tree/a012111a935e0dd8eb9d661fbbfb4110e55561d0/Transformations/test-data/UML):
   - `CityGML_3.0-workspaces-documents_shapechange-export.xml` (Recommended) - An optimized ShapeChange UML format. Produces much faster ShapeChange transformations.
      ```bash
      wget -O ./input/CityGML_3.0-workspaces-documents_shapechange-export.xml https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Transformations/test-data/UML/CityGML_3.0-workspaces-documents_shapechange-export.xml
      ```
   - `CityGML_3.0-workspaces-documents.eap` - Enterprise Architect (EA) format. Transformation requires Windows and following the [ShapeChange installation instructions](#dependencies) for enabeling Enterprise Architect models.
      ```bash
      wget -O ./input/CityGML_3.0-workspaces-documents.eap https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Transformations/test-data/UML/CityGML_3.0-workspaces-documents.eap
      ```
3. Choose one (or both) of the following ShapeChange configuration files based on your needs:
   - For CityOWL OWA: [./shapechange-configs/CityGML3.0_to_OWL_lite_config.xml](./shapechange-configs/CityGML3.0_to_OWL_lite_config.xml)
   - For CityOWL CWA: [./shapechange-configs/CityGML3.0_to_OWL_config.xml](./shapechange-configs/CityGML3.0_to_OWL_config.xml)
   - If using the EA format, comment line 4 and uncomment line 3 in the config.
      ```xml
      <parameter name="inputModelType" value="EA7"/>
      <!-- <parameter name="inputModelType" value="SCXML"/> -->
      ```
4. Download this configuration file dependency:
      ```bash
      wget -O ./StandardMapEntries_iso19107-owl.xml https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Transformations/ShapeChange/StandardMapEntries_iso19107-owl.xml
      ```
5. Transform with ShapeChange. For example, to transform using the OWA configuration (Update paths in brackets):
      ```bash
      java -jar [path to ShapeChange jar] -Dfile.encoding=UTF-8 \
         -c ./input/CityGML3.0_to_OWL_lite_config.xml \
         -x '$input$' './input/CityGML_3.0-workspaces-documents_shapechange-export.xml' \
         -x '$output$' 'stage-1'
      ```
6. Next we must patch and modify the generated ontologies. Run the UD-Graph ontology patcher on each generated ontology:
      ```bash
      ./patch-ontologies.sh
      ```
7. Add CodeLists. Currently, the shapechange rule to generate codelists automatically as SKOS concept schemes does not work with the CityGML CM. These have been created manually as an external files and must be added to each ontology. This can be done by using the AddTriples script:
   ```bash
   ./add-codes.sh
   ```
8. FIXME - union transformation
9. FIXME - gml:boundedby -> hasGeometry
<!-- 9.  FIXME - double check alignments -->
1.  Update ADE namespaces. The Document and Workspace ADE ontologies contain incorrect URIs. To fix this, perform a ctrl+F replace in your favorite text editor or IDE
   1. For the Document ontology, 
      - Replace `https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Ontologies/CityGML/3.0/document`
      - With `https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Ontologies/Document/3.0/document`. 
   2. For the Workspace ontology, 
      - Replace `https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Ontologies/CityGML/3.0/workspace`
      - With `https://dataset-dl.liris.cnrs.fr/rdf-owl-urban-data-ontologies/Ontologies/Workspace/3.0/workspace`
2.  Other
3.  (Optional) test with [Protégé](https://protege.stanford.edu/software.php#desktop-protege) that the ontologies load.
   1. Test with and without importing external ontologies online.
   2. Test ontologies are logically sound with a reasoner.
