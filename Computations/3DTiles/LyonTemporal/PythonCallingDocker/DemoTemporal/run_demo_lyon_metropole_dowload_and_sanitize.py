import os
import sys
import logging
import demo_workflow_temporal as workflow


if __name__ == '__main__':
    download = workflow.demo_download
    download.create_output_dir()

    logger = logging.getLogger(__name__)
    log_filename = os.path.join(download.get_output_dir(),
                               'demo_lyon_metropole_dowload_and_sanitize.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    download.run()
    download.assert_output_files_exist()
    logging.info("Resulting files: ")
    [ logging.info( "   " + file) for file in download.get_resulting_filenames() ]

