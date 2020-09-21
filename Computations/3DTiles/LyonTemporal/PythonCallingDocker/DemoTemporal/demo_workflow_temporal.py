import sys
import logging
import time
from demo_lyon_metropole_dowload_and_sanitize_temporal \
  import DemoLyonMetropoleDowloadAndSanitizeTemporal
from demo_split_buildings_temporal import DemoSplitBuildingsTemporal
from demo_strip_attributes import DemoStrip
from demo_extract_building_dates import DemoExtractBuildingDates
from demo_load_3dcitydb import DemoLoad3DCityDB
from demo_tiler_temporal import DemoTilerTemporal
from demo_3dcitydb_server import Demo3dCityDBServer

# Definition of the workflow by defining its nodes and connections
demo_download = DemoLyonMetropoleDowloadAndSanitizeTemporal('BATI', 'stage_1')

demo_split = DemoSplitBuildingsTemporal()
demo_split.set_results_dir('stage_2') 
demo_split.set_input_demo(demo_download)

demo_strip = DemoStrip()
demo_strip.set_results_dir('stage_3') 
demo_strip.set_input_demo(demo_split)

demo_extract = DemoExtractBuildingDates()
demo_extract.set_results_dir('stage_4') 
demo_extract.set_input_demo(demo_strip)

demo_db_server = Demo3dCityDBServer()

demo_load = DemoLoad3DCityDB()
demo_load.set_results_dir('stage_5') 
demo_load.set_input_demo(demo_strip)

demo_tiler = DemoTilerTemporal()
demo_tiler.set_results_dir('stage_6') 
demo_tiler.set_input_demo(demo_extract)
