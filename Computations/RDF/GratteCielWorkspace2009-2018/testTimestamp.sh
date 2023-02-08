#!/bin/sh

# python AddTimeStamps.py \
#     ../test-data/RDF/historicalSuccession_CityGML_3.0_v1.ttl \
#     ./historicalSuccession_v1.ttl \
#     2000-01-01T00:00:00 2000-01-01T00:00:00 \
#     -d

# python AddTimeStamps.py \
#     ../test-data/RDF/historicalSuccession_CityGML_3.0_v2.ttl \
#     ./historicalSuccession_v2.ttl \
#     2001-01-01T00:00:00 2001-01-01T00:00:00 \
#     -d

### cgml 3

python AddTimeStamps.py \
    --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2009_split.ttl \
    ./GratteCiel_2009_split.ttl \
    2009-01-01T00:00:00 2009-01-01T00:00:00 \
    -d

python AddTimeStamps.py \
    --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2012_split.ttl \
    ./GratteCiel_2012_split.ttl \
    2012-01-01T00:00:00 2012-01-01T00:00:00 \
    -d
    
python AddTimeStamps.py \
    --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2009_alt_split.ttl \
    ./GratteCiel_2009_alt_split.ttl \
    2010-01-01T00:00:00 2010-01-01T00:00:00 \
    -d

python AddTimeStamps.py \
    --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2012_alt_split.ttl \
    ./GratteCiel_2012_alt_split.ttl \
    2013-01-01T00:00:00 2013-01-01T00:00:00 \
    -d

python AddTimeStamps.py \
    --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
    ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2015_split.ttl \
    ./GratteCiel_2015_split.ttl \
    2015-01-01T00:00:00 2015-01-01T00:00:00 \
    -d

# python AddTimeStamps.py \
#     --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
#     ../../Datasets/GratteCiel_Workspace_2009_2018/3.0/GratteCiel_2018_split.ttl \
#     ./GratteCiel_2018_split.ttl \
#     2018-01-01T00:00:00 2018-01-01T00:00:00 \
#     -d

### cgml 2

# python AddTimeStamps.py \
#     --core-uri 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/CityGML/2.0/core#' \
#     --feature-member-property 'CityModel.cityObjectMember' \
#     --from-property 'AbstractCityObject.creationDate' \
#     --to-property 'AbstractCityObject.terminationDate' \
#     --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
#     ../../Datasets/GratteCiel_Workspace_2009_2018/2.0/GratteCiel_2009_split.ttl \
#     ./GratteCiel_2009_split.ttl \
#     2009-01-01T00:00:00 2009-01-01T00:00:00 \
#     -d

# python AddTimeStamps.py \
#     --core-uri 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/CityGML/2.0/core#' \
#     --feature-member-property 'CityModel.cityObjectMember' \
#     --from-property 'AbstractCityObject.creationDate' \
#     --to-property 'AbstractCityObject.terminationDate' \
#     --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
#     ../../Datasets/GratteCiel_Workspace_2009_2018/2.0/GratteCiel_2012_split.ttl \
#     ./GratteCiel_2012_split.ttl \
#     2012-01-01T00:00:00 2012-01-01T00:00:00 \
#     -d
    
# python AddTimeStamps.py \
#     --core-uri 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/CityGML/2.0/core#' \
#     --feature-member-property 'CityModel.cityObjectMember' \
#     --from-property 'AbstractCityObject.creationDate' \
#     --to-property 'AbstractCityObject.terminationDate' \
#     --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
#     ../../Datasets/GratteCiel_Workspace_2009_2018/2.0/GratteCiel_2009_alt_split.ttl \
#     ./GratteCiel_2009_alt_split.ttl \
#     2010-01-01T00:00:00 2010-01-01T00:00:00 \
#     -d

# python AddTimeStamps.py \
#     --core-uri 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/CityGML/2.0/core#' \
#     --feature-member-property 'CityModel.cityObjectMember' \
#     --from-property 'AbstractCityObject.creationDate' \
#     --to-property 'AbstractCityObject.terminationDate' \
#     --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
#     ../../Datasets/GratteCiel_Workspace_2009_2018/2.0/GratteCiel_2012_alt_split.ttl \
#     ./GratteCiel_2012_alt_split.ttl \
#     2013-01-01T00:00:00 2013-01-01T00:00:00 \
#     -d

# python AddTimeStamps.py \
#     --core-uri 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/CityGML/2.0/core#' \
#     --feature-member-property 'CityModel.cityObjectMember' \
#     --from-property 'AbstractCityObject.creationDate' \
#     --to-property 'AbstractCityObject.terminationDate' \
#     --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
#     ../../Datasets/GratteCiel_Workspace_2009_2018/2.0/GratteCiel_2015_split.ttl \
#     ./GratteCiel_2015_split.ttl \
#     2015-01-01T00:00:00 2015-01-01T00:00:00 \
#     -d

# python AddTimeStamps.py \
#     --core-uri 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/CityGML/2.0/core#' \
#     --feature-member-property 'CityModel.cityObjectMember' \
#     --from-property 'AbstractCityObject.creationDate' \
#     --to-property 'AbstractCityObject.terminationDate' \
#     --t-entity-property 'https://raw.githubusercontent.com/VCityTeam/UD-Graph/master/Ontologies/Time/time-extension#hasExistenceTime' \
#     ../../Datasets/GratteCiel_Workspace_2009_2018/2.0/GratteCiel_2018_split.ttl \
#     ./GratteCiel_2018_split.ttl \
#     2018-01-01T00:00:00 2018-01-01T00:00:00 \
#     -d