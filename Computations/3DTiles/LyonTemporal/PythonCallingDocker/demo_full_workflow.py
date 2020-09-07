import logging
from demo_lyon_metropole_dowload_and_sanitize import DemoLyonMetropoleDowloadAndSanitize
from demo_split_buildings import DemoSplitBuildings
from demo_strip_attributes import DemoStrip

# Definition of the workflow by defining its nodes and connections
demo_download = DemoLyonMetropoleDowloadAndSanitize('BATI', 'stage_1')

demo_split = DemoSplitBuildings()
demo_split.set_results_dir('stage_2') 
demo_split.set_input_demo(demo_download)

demo_strip = DemoStrip()
demo_strip.set_results_dir('stage_3') 
demo_strip.set_input_demo(demo_split)


if __name__ == '__main__':
    # The full pipeline
    demo_download.run()
    demo_split.run()
    demo_strip.run()
    logging.info("Resulting files: ")
    logging.info(demo_split.get_resulting_filenanes())

    # demo_split_buildings
    # demo_strip_attributes
    # demo_extract_building_dates
    # demo_3dcitydb_server is just a test and produces no output
    # demo_load_3dcitydb
