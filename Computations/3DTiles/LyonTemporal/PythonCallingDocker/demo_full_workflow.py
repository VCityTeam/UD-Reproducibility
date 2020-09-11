import logging
from demo_lyon_metropole_dowload_and_sanitize import DemoLyonMetropoleDowloadAndSanitize
from demo_split_buildings import DemoSplitBuildings
from demo_strip_attributes import DemoStrip
from demo_extract_building_dates import DemoExtractBuildingDates
from demo_load_3dcitydb import DemoLoad3DCityDB
from demo_temporal_tiler import DemoTemporalTiler

# Definition of the workflow by defining its nodes and connections
demo_download = DemoLyonMetropoleDowloadAndSanitize('BATI', 'stage_1')

demo_split = DemoSplitBuildings()
demo_split.set_results_dir('stage_2') 
demo_split.set_input_demo(demo_download)

demo_strip = DemoStrip()
demo_strip.set_results_dir('stage_3') 
demo_strip.set_input_demo(demo_split)

demo_extract = DemoExtractBuildingDates()
demo_extract.set_results_dir('stage_4') 
demo_extract.set_input_demo(demo_strip)

demo_load = DemoLoad3DCityDB()
demo_load.set_results_dir('stage_5') 
demo_load.set_input_demo(demo_strip)

demo_tiler = DemoTemporalTiler()
demo_tiler.set_results_dir('stage_6') 
demo_tiler.set_input_demo(demo_extract)


if __name__ == '__main__':
    # The full pipeline
    demo_download.run()
    logging.info(demo_download.get_resulting_filenames())
    demo_split.run()
    logging.info(demo_split.get_resulting_filenames())
    demo_strip.run()
    logging.info(demo_strip.get_resulting_filenames())
    demo_extract.run()
    logging.info(demo_extract.get_resulting_filenames())
    # demo_3dcitydb_server is just a test and produces no output
    demo_load.run()
    logging.info("Resulting files: ")
    logging.info(demo_load.get_resulting_filenames())

