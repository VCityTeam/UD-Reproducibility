import os
import sys
import logging
from docker_py3dtiles import DockerPy3dtiles


class DockerTilerBase(DockerPy3dtiles):
    def __init__(self):
        super().__init__()
        self.db_config_filenames = list()

    def assert_ready_for_run(self):
        if not self.db_config_filenames:
            logging.info('Missing database configuration files for running. '
                         'Please set up at least two of them.')
            sys.exit(1)

    def add_db_config_file(self, db_config_file):
        if not os.path.isfile(db_config_file):
            logging.info(f'Database configuration file'
                         f' {db_config_file} not found. Exiting')
            sys.exit(1)
        self.db_config_filenames.append(db_config_file)

    def generate_configuration_file(self, vintage, db_config, output_file_basename):
        """
        The Tiler requires a configuration file describing the database
        access it will use. This file has an ad-hoc xml format that this
        method generates out .  
        """
        target_file = os.path.join(self.get_mounted_input_directory(),
                                   output_file_basename)
        with open(target_file, 'w') as output:
            output.write(f'PG_HOST: {db_config["PG_HOST"]}\n')
            output.write(f'PG_PORT: {db_config["PG_PORT"]}\n')
            output.write(f'PG_NAME: {db_config["PG_NAME"]}\n')
            output.write(f'PG_USER: {db_config["PG_USER"]}\n')
            output.write(f'PG_PASSWORD: {db_config["PG_PASSWORD"]}\n')
            output.write(f'PG_VINTAGE: {vintage}\n')
