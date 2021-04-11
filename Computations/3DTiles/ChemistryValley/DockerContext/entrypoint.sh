#!/bin/bash
set -x
pwd

python3.7 run_lyon_metropole_dowload_and_sanitize_static.py   # result in junk/stage_1
python3.7 run_split_buildings_static.py                       # result in junk/stage_2
python3.7 run_strip_attributes_static.py                      # result in junk/stage_3 
python3.7 run_load_3dcitydb_static.py                         # result in postgres-data-static/
python3.7 run_tiler_static.py
cp -r junk/ /Output
