# #!/bin/sh

# echo '=== cleaning workspace ==='
# ./clean.sh

# echo '=== download input ==='
# mkdir ./input
# wget -O ./input/CityGML_3.0-workspaces-documents_shapechange-export.xml \
#     https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Transformations/test-data/UML/CityGML_3.0-workspaces-documents_shapechange-export.xml

# echo '=== stage 1 ==='
# java -jar ./ShapeChange-3.0.0.jar -Dfile.encoding=UTF-8 \
#     -c ./shapechange-configs/CityGML3.0_to_OWL_lite_config.xml \
#     -x '$input$' './input/CityGML_3.0-workspaces-documents_shapechange-export.xml' \
#     -x '$output$' 'stage-1'

echo '=== stage 2 ==='
./patch-ontologies.sh

echo '=== stage 3 ==='
./update-triples.sh

echo 'Done!'
