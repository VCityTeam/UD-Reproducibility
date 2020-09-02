## Pre-requisites
 - [install Python3.7](https://www.python.org/)

## Configuration step
Configure the `demo_configuration.py` file with the output_directory, the
vintages (currently only 2009, 2012 and 2015 are available for the Grand Lyon) 
and the borough you want to include (e.g. LYON_1ER, VILLEURBANNE, etc.). You
must also provide one database configuration per vintage (these databases
hold the citygml data). 

Notes:
 * in order to configure `PG_HOST` i.e. the IP number of the host machine, you
   might use (on a linux machine) the `hostname -I` command.
 * the `PG_HOST`, although present in three configuration files, must be the same shared IP number value for the three configuration files. This is because the three (3dCity) databases used by the worklow run on the same host...

## Installing dependencies
Then, running the workflow goes:
```
$ git rev-parse --show-toplevel
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```
If you wan to run unit tests:
```
(venv)$ git rev-parse --show-toplevel
(venv)$ pip install pytest pytest-ordering pytest-dependency
(venv)$ pytest
```

FIXME: the rest is under construction

## Running the workflow

### Manual step by step run

```
(venv)$ git rev-parse --show-toplevel
(venv)$ python lyon_metropole_dowload_and_sanitize.py
(venv)$ python docker_split_buildings.py
(venv)$ python demo_strip_attributes.py
(venv)$ python demo_extract_building_dates.py
(venv)$ python demo_3dcitydb_server.py
(venv)$ python demo_load_3dcitydb.py
```
The resulting file hierarchy will be located in the `junk` sub-directory (as
configured by the `output_dir` variable of `demo_configuration.py`.


## Developers notes
 * Debugging of a container
   ```
   docker run -v `pwd`/junk/LYON_1ER_2009/:/Input -v `pwd`/junk_split/:/Output -it liris:3DUse /bin/bash
   root@ splitCityGMLBuildings --input-file /Input/LYON_1ER_BATI_2009.gml --output-file LYON_1ER_BATI_2009_splited.gml --output-dir /Output/
   ```

## Issues

### Bug: extractBuildingDates stage fails on Villeurbanne data
The following run fails
```
docker run -v `pwd`:/Input --workdir /root/3DUSE/Build/src/utils/cmdline/ -t liris:3DUse extractBuildingDates --first_date 2009 --first_file /Input/junk/VILLEURBANNE_2009/VILLEURBANNE_BATI_2009.gml --second_date 2012 --second_file /Input/junk/VILLEURBANNE_2012/VILLEURBANNE_BATI_2012.gml --output_dir /Input/junk/2009_2012_Differences/VILLEURBANNE_2009-2012/
```
with the message:
```
CityGML first file loaded :/Input/junk/VILLEURBANNE_2009/VILLEURBANNE_BATI_2009.gml
CityGML second file loaded :/Input/junk/VILLEURBANNE_2012/VILLEURBANNE_BATI_2012.gml
Model 1: 
    Converting building: 455/455 
Done.
Model 2: 
    Converting building: 447/447 
Done.
Internal buildings pre-processing...
ERROR 1: TopologyException: found non-noded intersection between LINESTRING (1.8489e+06 5.17487e+06, 1.84892e+06 5.17488e+06) and LINESTRING (1.84891e+06 5.17488e+06, 1.84892e+06 5.17488e+06) at 1848907.2497562491 5174876.2345244605 191.31213515757889
```
This error seems related with postgis or gdal according to threads like:
 * [R wrapping of gdal](https://stackoverflow.com/questions/13662448/what-does-the-following-error-mean-topologyexception-found-non-nonded-intersec)
 * [r-spatial/sf issue](https://github.com/r-spatial/sf/issues/860)

### Debugging the importer exporter
 * The following proves that the database server is ok
   ```
   docker run -v `pwd`/:/InputConfig -it --entrypoint /bin/bash tumgis/3dcitydb-impexp:4.2.3

   apt-get update
   apt-get install postgresql postgresql-contrib
   psql -h 134.214.143.170 -p 5432 -U postgres -d citydb-full_lyon-2009 -c "\dt"
   # provide postgres as password
   .... # you will get some answer
   ```

 * The following single call reproduces the error:
    ```
    docker run -v `pwd`/:/InputConfig -v `pwd`/junk/LYON_2009_Stripped:/InputFiles -it tumgis/3dcitydb-impexp:4.2.3 -config /InputConfig/3dCityDBImpExpConfig2009.xml -import /InputFiles/LYON_1ER_BATI_2009_splited_stripped.gml
    ```
