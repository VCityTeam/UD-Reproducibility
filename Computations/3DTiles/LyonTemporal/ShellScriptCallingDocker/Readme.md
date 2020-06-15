## Pre-requisites
 - bash/sh shellscript interpreters
 - [install Docker](https://docs.docker.com/install/)
 - [install Python3](https://www.python.org/)

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
(venv)$ pip install -r requirements.txt   # Because we need j2 on the cli
```

## Running the worflow
```
(venv) ./DockerComputeLyonCityEvolution.sh <some_output_dir>
```
The resulting tile-set will be located in the `some_output_dir/Result` sub-directory.

If you whish to measure the execution time and log the execution traces you might use
```
time ./DockerComputeLyonCityEvolution.sh some_output_dir > run.log 2>&1 &
tail -f run.log
```

## Improving things (TODO list)
 * Automatize the configuration of the IP number that is hardwired in many configuration files. Note that the command `hostname -I` is not even portable. Maybe we should go for docker in docker and dockerise the main shell script ? Will that _really_ slow things down ?
 * At the beginning of the pipeline Bron and Villeurbanne are dealt with. Yet, at some point they vanish from the workflow. Fix that !
