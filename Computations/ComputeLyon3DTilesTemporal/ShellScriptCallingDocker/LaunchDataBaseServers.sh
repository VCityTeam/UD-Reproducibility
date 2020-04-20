#!/bin/bash

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# FIXME : presistence with "local directory mounts"
#
# TIP: try the syntax documented [here](https://github.com/tum-gis/3dcitydb-docker-postgis#bind-mounts) 
#
# Objective: we want to persit the build database as a set of (database) 
# files in order to transmit them to some partner (in other terms, we
# want to have at hand the result of the database integration). 
#
# What was tried: if we try to follow e.g. 
#   https://stackoverflow.com/questions/46504902/postgres-docker-persistence
# the the --mount option seems ineffective. For example is we run
#   mkdir -p database-2009
#   docker run -dt --name citydb-container-2009 -p 5432:5432 \
#     -e "CITYDBNAME=citydb-full_lyon-2009" \
#     -e "SRID=3946" -e "SRSNAME=espg:3946" \
#     -e "POSTGRES_USER=postgres" -e "POSTGRES_PASSWORD=postgres" \
#     --mount src="$(pwd)"/data,target=/var/lib/postgresql/,type=bind \
#     tumgis/3dcitydb-postgis
#   docker inspect citydb-container-2009
# (and look at the "Mounts" entry) then everything looks ok. Yet after
# uploading the DB, the database-2009 directory remains empty...
#
# Some clues:
# * run 
#   docker run -it --name citydb-container-2009 -p 5432:5432 \
#   -e "CITYDBNAME=citydb-full_lyon-2009"   -e "SRID=3946" \
#   -e "SRSNAME=espg:3946"   -e "POSTGRES_USER=postgres" \
#   -e "POSTGRES_PASSWORD=postgres"  tumgis/3dcitydb-postgis bash
# * then when running
#      docker inspect tumgis/3dcitydb-postgis
#   the Volumes or the Mounts entries tell us that /var/lib/postgresql/data
#   is a docker volume (the way docker does persistence, refer e.g. to
#   https://linuxhint.com/dockerfile_volumes/ )
# * 3dcitydb-postgis container is based on postgres version 11 container as
#   indicated by
#   https://github.com/tum-gis/3dcitydb-docker-postgis/blob/master/v4.0.2/Dockerfile#L7
# * The postgres docker images are documentend here
#      https://hub.docker.com/_/postgres
#   and version 11 indeed defines /var/lib/postgresql/data as a volume as
#   indicated here
#      https://github.com/docker-library/postgres/blob/0d0485cb02e526f5a240b7740b46c35404aaf13f/11/Dockerfile#L169
# References
# - https://docs.docker.com/storage/bind-mounts/

echo "Launching the (dockerized) 3dcitydb-postgis database servers."
./LaunchDataBaseServerFirst.sh
./LaunchDataBaseServerSecond.sh
./LaunchDataBaseServerThird.sh

echo -n "   Waiting for tumgis/3dcitydb-postgis to spin off..."
sleep 10
echo "done."
