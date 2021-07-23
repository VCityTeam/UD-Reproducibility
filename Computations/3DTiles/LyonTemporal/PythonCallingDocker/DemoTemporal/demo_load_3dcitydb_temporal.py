import os
import sys
import logging
from demo_temporal import DemoWithDataBasesTemporal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from docker_load_3dcitydb import DockerLoad3DCityDB


class DemoLoad3DCityDBTemporal(DemoWithDataBasesTemporal):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the DockerLoad3DCityDB algorithms for designating its input
    directories and filenames
    """
    def __init__(self):
        super().__init__()    # Calling the DemoTemporal constructor
        super().__init_databases__()

    def run(self, log_filename):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("DemoLoad3DCityDB misses some of its input files: exiting")
            sys.exit(1)
        self.create_output_dir()   # Just making sure

        for vintage in self.vintages:
            logging.info(f'Importation for vintage {str(vintage)}: starting.')
            d = DockerLoad3DCityDB(self.databases[vintage])
            
            inputs = list(map(os.path.abspath, input.get_vintage_resulting_filenames(vintage)))
            d.set_files_to_import(inputs)
            logging.info(f'Files set for importation: {inputs}')
            
            d.run()
            d.check_log_result(log_filename)
            logging.info(f'Importation for vintage {str(vintage)}: done.')
