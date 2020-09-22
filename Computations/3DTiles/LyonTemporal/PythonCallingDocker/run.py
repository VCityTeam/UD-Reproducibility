import os
import logging


def run_demo_lyon_metropole_dowload_and_sanitize(download):
   download.create_output_dir()

   logger = logging.getLogger(__name__)
   logging.basicConfig(level=logging.DEBUG,
                       format='%(asctime)s %(levelname)-8s %(message)s',
                       datefmt='%a, %d %b %Y %H:%M:%S',
                       filename=os.path.join(
                           download.get_output_dir(),
                           'demo_lyon_metropole_dowload_and_sanitize.log'),
                       filemode='w')

   download.run()
   download.assert_output_files_exist()
   logging.info("Resulting files: ")
   [ logging.info( "   " + file) for file in download.get_resulting_filenames() ]

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

import logging
import os
import sys


def run_demo_strip_attributes(strip):
    strip.create_output_dir()

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.join(strip.get_output_dir(),
                                              'demo_strip_buildings.log'),
                        filemode='w')
    logging.info("Starting to strip files.")

    strip.run()
    if not strip.assert_output_files_exist():
        logging.info("Some output is missing: exiting.")
        sys.exit()
    logging.info("Resulting stripped files:")
    [ logging.info( "   " + file) for file in strip.get_resulting_filenames() ]
