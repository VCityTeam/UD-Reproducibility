## This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

mkdir -p WebDemos
cd WebDemos
git clone https://github.com/jailln/UDV.git
mv UDV UD-Viz-Temporal-Limonest
cd UD-Viz-Temporal-Limonest
git checkout UDV-temporal
cd UDV-Core
./install.sh
