import os
import sys
import logging
import demo_workflow_temporal as workflow


if __name__ == '__main__':
    extract = workflow.demo_extract
    extract.create_output_dir()

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.join(extract.get_output_dir(),
                                              'demo_extract_building_dates.log'),
                        filemode='w')
    logging.info("Starting to extract building dates.")   

    extract.run()
    if not extract.assert_output_files_exist():
        logging.info("Some output is missing: exiting.")
        sys.exit()
    logging.info("Resulting extracted building dates files:")
    [ logging.info( "   " + file) for file in extract.get_resulting_filenames() ]

