# !/bin/sh

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

echo "Halting the 3dcitydb-postgis database servers."
###### Stop the 3dcitydb-postgis
echo "  Stoping containers:"
docker stop citydb-container-2009 citydb-container-2012 citydb-container-2015
echo "  Removing containers:"
docker rm   citydb-container-2009 citydb-container-2012 citydb-container-2015
echo "3dcitydb-postgis database servers now halted."