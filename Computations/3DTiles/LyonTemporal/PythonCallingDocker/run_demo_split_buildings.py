import os
import sys
import logging


def run_demo_split_buildings(split): 
    split.create_output_dir()

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.join(split.get_output_dir(),
                                              'demo_split_buildings.log'),
                        filemode='w')
    logging.info("Starting to split files.")

    split.run()
    if not split.assert_output_files_exist():
        logging.info("Some output is missing: exiting.")
        sys.exit()
    logging.info("Resulting split files:")
    [ logging.info( "   " + file) for file in split.get_resulting_filenames() ]

