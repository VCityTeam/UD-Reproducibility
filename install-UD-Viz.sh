## This script only works when invocated where it stands...
cd "$(dirname "$0")" || exit

mkdir -p WebDemos
cd WebDemos
git clone https://github.com/MEPP-team/UD-Viz.git
cd UD-Viz/UD-Viz-Core
npm install
npm run build 
