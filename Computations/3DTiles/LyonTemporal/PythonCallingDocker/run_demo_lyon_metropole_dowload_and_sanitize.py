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

