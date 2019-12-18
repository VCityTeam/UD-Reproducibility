## This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

mkdir -p WebDemos/DataStore
cd WebDemos/DataStore
echo "Do not edit this automatically generated file (can be overwritten)." > Readme.md
echo " " >> Readme.md
echo "This directory holds data accessed through their URL." >> Readme.md
echo "It mainly serves 3dTiles tilesets (generated somewhere else". >> Readme.md
