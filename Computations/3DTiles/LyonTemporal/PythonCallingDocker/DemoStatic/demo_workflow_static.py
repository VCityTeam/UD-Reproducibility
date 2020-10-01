import sys
import os
import logging
import time

from demo_lyon_metropole_dowload_and_sanitize_static \
    import DemoLyonMetropoleDowloadAndSanitizeStatic
from demo_split_buildings_static import DemoSplitBuildingsStatic
from demo_strip_attributes_static import DemoStripStatic
from demo_load_3dcitydb_static import DemoLoad3DCityDBStatic
from demo_tiler_static import DemoTilerStatic
from demo_3dcitydb_server_static import Demo3dCityDBServerStatic

# Definition of the workflow by defining its nodes and connections
demo_download = DemoLyonMetropoleDowloadAndSanitizeStatic('BATI', 'stage_1')

demo_split = DemoSplitBuildingsStatic()
demo_split.set_results_dir('stage_2') 
demo_split.set_input_demo(demo_download)

demo_strip = DemoStripStatic()
demo_strip.set_results_dir('stage_3') 
demo_strip.set_input_demo(demo_split)

demo_db_server = Demo3dCityDBServerStatic()

demo_load = DemoLoad3DCityDBStatic()
demo_load.set_results_dir('stage_4') 
demo_load.set_input_demo(demo_strip)

demo_tiler = DemoTilerStatic()
demo_tiler.set_results_dir('stage_5') 
demo_tiler.set_input_demo(demo_strip) # Hoping the load import was ok.
