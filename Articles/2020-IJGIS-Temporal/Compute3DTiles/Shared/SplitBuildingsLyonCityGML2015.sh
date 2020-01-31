# !/bin/sh

# This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

# Check that parameters are correctly provided
if [ $# != 2 ]
  then
    echo "Awaited parameters: "
    echo "  1. the input folder."
    echo "  2. the output folder."
    exit 1
fi

# For 2015 we simply re-cast the file hierachy out of the original GrandLyon
# folders organization
mkdir ${2}
cp ${1}/LYON_1ER_2015/LYON_1ER_BATI_2015.gml   ${2}/
cp ${1}/LYON_2EME_2015/LYON_2EME_BATI_2015.gml ${2}/
cp ${1}/LYON_3EME_2015/LYON_3EME_BATI_2015.gml ${2}/
cp ${1}/LYON_4EME_2015/LYON_4EME_BATI_2015.gml ${2}/
cp ${1}/LYON_5EME_2015/LYON_5EME_BATI_2015.gml ${2}/
cp ${1}/LYON_6EME_2015/LYON_6EME_BATI_2015.gml ${2}/
cp ${1}/LYON_7EME_2015/LYON_7_BATI_2015.gml    ${2}/LYON_7EME_BATI_2015.gml
cp ${1}/LYON_8EME_2015/LYON_8EME_BATI_2015.gml ${2}/
cp ${1}/LYON_9EME_2015/LYON_9EME_BATI_2015.gml ${2}/

