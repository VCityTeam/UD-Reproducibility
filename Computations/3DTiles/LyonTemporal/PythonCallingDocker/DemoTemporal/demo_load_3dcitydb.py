import os
import sys
import logging
import jinja2
import time

from demo_temporal import DemoWithDataBasesTemporal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from docker_load_3dcitydb import DockerLoad3DCityDB
from demo_load_3dcitydb_base import DemoLoad3DCityDBBase


class DemoLoad3DCityDB(DemoWithDataBasesTemporal, DemoLoad3DCityDBBase):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the DockerLoad3DCityDB algorithms for designating its input
    directories and filenames
    """
    
    @staticmethod
    def __get_vintage_configuration_filename(vintage):
        return '3dCityDBImpExpConfig' + str(vintage) + '.xml'

    def __init__(self):
        super().__init__()
        super().__init_databases__()
        # Generate the 3dCityDB-importer ad-hoc configuration files that will be 
        # transmitted to the 
        for vintage in self.vintages:
            DemoLoad3DCityDBBase.generate_configuration_file(
                self.databases[vintage],
                DemoLoad3DCityDB.__get_vintage_configuration_filename(vintage))

    def run(self):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("DemoLoad3DCityDB misses some of its input files: exiting")
            sys.exit(1)
        self.create_output_dir()   # Just making sure

        for vintage in self.vintages:
            logging.info(f'Importation for vintage {str(vintage)}: starting.')
            d = DockerLoad3DCityDB()

            inputs = list(map(os.path.abspath, input.get_vintage_resulting_filenames(vintage)))
            d.set_files_to_import(inputs)
            logging.info(f'Files set for importation: {inputs}')

            d.set_configuration_filename(
                os.path.abspath(DemoLoad3DCityDB.__get_vintage_configuration_filename(vintage)))
            d.run()
            logging.info(f'Importation for vintage {str(vintage)}: done.')

    def check_log_result(self, log_filename):
        # Preconditions
        if not os.path.isfile(log_filename):
            logging.info(f'Log file {log_filename} not found. Exiting')
            sys.exit(1)

        # Establish what importations must be checked:
        input = self.get_input_demo()
        last_loaded_vintage_filename = dict()
        for filename in input.get_resulting_filenames():
            file_basename = os.path.basename(filename)
            for vintage in self.vintages:
                vintage = str(vintage)
                if vintage in file_basename:
                    last_loaded_vintage_filename[vintage] = file_basename
        if not last_loaded_vintage_filename:
             logging.info('No filenames to look for in importation logs. Exiting')
             sys.exit(1)
        logging.info('Looking for following files in importation logs:')
        for key, value in last_loaded_vintage_filename.items():
            logging.info(f'   checking logs for vintage {key} and file {value}.')

        # Proceed with checks:
        checked_assertions = 0
        with open(log_filename, 'r') as f:
            for line in f.readlines():
                if 'Database import successfully finished' in line:
                    for vintage in self.vintages:
                        vintage = str(vintage)
                        if last_loaded_vintage_filename[vintage] in line:
                            logging.info(f'Vintage {vintage} correctly imported.')
                            checked_assertions +=1
        if checked_assertions == len(self.vintages):
            return True
        return False
 
