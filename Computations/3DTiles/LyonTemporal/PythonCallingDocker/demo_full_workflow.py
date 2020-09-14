import sys
import logging
import time
from demo_lyon_metropole_dowload_and_sanitize import DemoLyonMetropoleDowloadAndSanitize
from demo_split_buildings import DemoSplitBuildings
from demo_strip_attributes import DemoStrip
from demo_extract_building_dates import DemoExtractBuildingDates
from demo_load_3dcitydb import DemoLoad3DCityDB
from demo_temporal_tiler import DemoTemporalTiler
from demo_3dcitydb_server import Demo3dCityDBServer

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

demo_db_server = Demo3dCityDBServer()

demo_load = DemoLoad3DCityDB()
demo_load.set_results_dir('stage_5') 
demo_load.set_input_demo(demo_strip)

demo_tiler = DemoTemporalTiler()
demo_tiler.set_results_dir('stage_6') 
demo_tiler.set_input_demo(demo_extract)


if __name__ == '__main__':
    # The full pipeline
    log_filename = 'demo_full_workflow.log'

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    logging.info("##################DemoFullWorkflow##### 1: Starting download.")
    demo_download.run()
    if not demo_download.assert_output_files_exist():
        logging.info("##################DemoFullWorkflow##### 1: Failed.")
        sys.exit(1)
    logging.info("##################DemoFullWorkflow##### 1: Resulting files: ")
    [ logging.info( "   " + file) for file in demo_download.get_resulting_filenames() ]
    logging.info("##################DemoFullWorkflow##### 1: Done.")


    logging.info("##################DemoFullWorkflow##### 2: Split files; start. ")
    demo_split.run()
    if not demo_split.assert_output_files_exist():
        logging.info("##################DemoFullWorkflow##### 2: Failed.")
        sys.exit(1)
    logging.info("##################DemoFullWorkflow##### 2: Resulting files.")
    [ logging.info( "   " + file) for file in demo_split.get_resulting_filenames() ]
    logging.info("##################DemoFullWorkflow##### 2: Done.")


    logging.info("##################DemoFullWorkflow##### 3: Strip files; start. ")
    demo_strip.run()
    if not demo_strip.assert_output_files_exist():
        logging.info("##################DemoFullWorkflow##### 3: Failed.")
        sys.exit(1)
    logging.info("##################DemoFullWorkflow##### 3: Resulting files.")
    [ logging.info( "   " + file) for file in demo_strip.get_resulting_filenames() ]
    logging.info("##################DemoFullWorkflow##### 3: Done.")


    logging.info("##################DemoFullWorkflow##### 4: Extract files; start. ")
    demo_extract.run()
    if not demo_extract.assert_output_files_exist():
        logging.info("##################DemoFullWorkflow##### 4: Failed.")
        sys.exit(1)
    logging.info("##################DemoFullWorkflow##### 4: Resulting files.")
    [ logging.info( "   " + file) for file in demo_extract.get_resulting_filenames() ]
    logging.info("##################DemoFullWorkflow##### 4: Done.")

    logging.info('##################DemoFullWorkflow##### 5: Starting databases.')
    demo_servers = Demo3dCityDBServer()
    demo_servers.run()
    time.sleep(120)
    logging.info('##################DemoFullWorkflow##### 5: Databases started')
    logging.info('##################DemoFullWorkflow##### 5: Importing files.')
    demo_load.run()
    if not demo_load.check_log_result(log_filename):
        logging.info('##################DemoFullWorkflow##### 5: Failed.')
        sys.exit(1)
    logging.info('##################DemoFullWorkflow##### 5: Done')

    logging.info('##################DemoFullWorkflow##### 6: Tiler starting.')
    demo_tiler.run()
    logging.info('##################DemoFullWorkflow##### 6: Tiler done.')
    logging.info('##################DemoFullWorkflow##### 6: Databases halted.')
    demo_servers.halt()
    logging.info('##################DemoFullWorkflow##### 6: Workflow ended.')
