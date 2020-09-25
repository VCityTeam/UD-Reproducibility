import sys
import os
import logging
import time

from demo_temporal import DemoTemporal
from demo_workflow_temporal import demo_download, demo_split, demo_strip, demo_extract
from demo_workflow_temporal import demo_db_servers
from demo_workflow_temporal import demo_load, demo_tiler


if __name__ == '__main__':
    # Run all the stages of the full pipeline
    DemoTemporal().create_output_dir()
    log_filename = os.path.join(DemoTemporal().get_output_dir(),
                                'demo_full_workflow.log')

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
    demo_db_servers.run()
    time.sleep(120)
    logging.info('##################DemoFullWorkflow##### 5: Databases started')
    logging.info('##################DemoFullWorkflow##### 5: Importing files.')
    try:
        demo_load.run(log_filename)
        logging.info('##################DemoFullWorkflow##### 5: Done')
    except:
        logging.info('##################DemoFullWorkflow##### 5: Failed.')
        demo_db_servers.halt()
        logging.info('##################DemoFullWorkflow##### Exiting.')
        sys.exit(1)
    
    logging.info('##################DemoFullWorkflow##### 6: Tiler starting.')
    demo_tiler.run()
    logging.info('##################DemoFullWorkflow##### 6: Tiler done.')
    logging.info('##################DemoFullWorkflow##### 6: Databases halted.')
    demo_db_servers.halt()
    logging.info('##################DemoFullWorkflow##### 6: Workflow ended.')
