import logging
import os
import sys
import demo_workflow_temporal as workflow


if __name__ == '__main__':
    strip = workflow.demo_strip
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
