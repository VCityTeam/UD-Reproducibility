import os
import sys
import logging
import time


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

        
def run_demo_load_3dcitydb(load, db_server):
    load.create_output_dir()
    db_server.create_output_dir()

    logger = logging.getLogger(__name__)
    log_filename = os.path.join(load.get_output_dir(), 'demo_load_3dcitydb.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    logging.info('Stage 1: starting database(s).')
    db_server.run()
    logging.info('Stage 1: done.')

    logging.info('Stage 2: waiting an extra 2 minutes for database(s) to spin off.')
    time.sleep(120)
    logging.info('Stage 2: done.')

    logging.info('Stage 3: importing files to database(s).')
    try:
        load.run(log_filename)
        logging.info('Stage 3: done')
    except:
        logging.info('Stage 3: importation failed')

    logging.info('Stage 4: halting database container(s).')
    db_server.halt()
    logging.info('Stage 4: done')


def run_demo_tiler(tiler, server):
    tiler.create_output_dir()
    server.create_output_dir()

    logger = logging.getLogger(__name__)
    log_filename = os.path.join(tiler.get_output_dir(), 'demo_tiler.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    logging.info('Stage 1: start databases wait.')
    server.run()
    logging.info('Stage 1: wait for 2 minutes for databases to spin off.')
    time.sleep(120)
    logging.info('Stage 1: done.')

    logging.info('Stage 2: computing the tiles.')
    try:
        tiler.run()
        logging.info('Stage 2: done.')
    except:
        logging.info('Stage 3: tiler failed.')

    logging.info('Stage 3: halting containers.')
    server.halt()
    logging.info('Stage 3: done')


