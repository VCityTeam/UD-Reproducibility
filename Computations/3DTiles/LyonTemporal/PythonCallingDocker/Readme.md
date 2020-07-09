## Pre-requisites
 - [install Python3.7](https://www.python.org/)

## Configuration step
Configure the three configuration files `DBConfig[2009|2012|2015].yml`.

Notes:
 * in order to configure PG_HOST i.e. the IP number of the host machine, you might use (on a linux machine) the `hostname -I` command.
 * the `PG_HOST`, although present in three configuration files, must be the same shared IP number value for the three configuration files. This is because the three (3dCity) databases used by the worklow run on the same host...

## Installing dependencies
Then, running the workflow goes:
```
$ virtualenv -p python3 venv
$ . venv/bin/activate
(venv)$ pip install -r requirements.txt
```
If you wan to run unit tests:
```
(venv)$ pip install pytest pytest-benchmark pytest-dependency
(venv)$ pytest
```

FIXME: the rest is under construction

## Running the worflow

### Manual step by step run

```
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

