## Pre-requisites
 - [install Python3.7](https://www.python.org/)

## Configuration step
Configure the three database configuration files `DBConfig[2009|2012|2015].yml`.

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
(venv)$ python docker_strip_attributes.py
(venv)$ python docker_extract_building_dates.py
```
The resulting file hierarchy will be located in the `junk` sub-directory.


## Developers notes
 * Debugging of a container
   ```
   docker run -v `pwd`/junk/LYON_1ER_2009/:/Input -v `pwd`/junk_split/:/Output -it liris:3DUse /bin/bash
   root@ splitCityGMLBuildings --input-file /Input/LYON_1ER_BATI_2009.gml --output-file LYON_1ER_BATI_2009_splited.gml --output-dir /Output/
   ```

## Issues
### Convert the configuration files to YAML
Merge the three configuration files in a single one using a YAML syntax.
Extract the loading of that file (Docker3DCityDBServer::load_config_file)
from the Docker3DCityDBServer class and pass the loaded dictionnary to
the Docker3DCityDBServer::__init__ constructor.
This will facilitate the Airflow/Prefect version that won't be able
to use a configuration file but will be handled over parameters.

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
