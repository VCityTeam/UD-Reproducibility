import os
import sys
import logging
from docker_py3dtiles import DockerPy3dtiles
import demo_configuration as demo


class DockerTemporalTiler(DockerPy3dtiles):
    def __init__(self):
        super().__init__()
        self.vintages = list()
        self.db_config_files = list()

    def assert_ready_for_run(self):
        if not self.vintages:
            logging.info('Missing vintages for running. Please specify at '
                         'least two vintages.')
            sys.exit(1)
        if not self.db_config_files:
            logging.info('Missing database configuration files for running. '
                         'Please set up at least two of them.')
            sys.exit(1)
        if len(self.db_config_files) != len(self.vintages):
            logging.info('Please specify as many database configuration '
                         'files as vintages.')
            sys.exit(1)

    def set_vintages(self, vintages):
        if not isinstance(vintages, list):
            logging.info('set_vintages() waits for a list of vintages.')
            sys.exit(1)
        if len(vintages) < 2:
            logging.info('You must provide at list two vintages.')
            sys.exit(1)
        self.vintages = vintages

    def add_vintage(self, vintage):
        self.vintages.append(vintage)

    def set_db_config_files(self, db_config_files):
        if not isinstance(db_config_files, list):
            logging.info('set_db_config_files() waits for a list of vintages.')
            sys.exit(1)
        if len(db_config_files) < 2:
            logging.info('You must provide at list two database configuration '
                         'files.')
            sys.exit(1)
        self.db_config_files = db_config_files

    def add_db_config_file(self, db_config_file):
        if not os.path.isfile(db_config_file):
            logging.info(f'Database configuration file'
                         f' {db_config_file} not found. Exiting')
            sys.exit(1)
        self.db_config_files.append(db_config_file)

    def get_command(self):
        self.assert_ready_for_run()
        # The Tiler to run, see ../Docker/CityTiler-DockerContext/entrypoint.py
        command = 'TemporalTiler '
        command += '--db_config_path '
        for db_config in self.db_config_files:
            command += db_config + ' '
        command += '--time_stamp '
        for vintage in self.vintages:
            command += str(vintage) + ' '


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    d = DockerTemporalTiler()

    d.set_db_config_files(demo.db_config_files)
    d.set_vintages(demo.vintages)

    graph_difference_absolute_path = os.path.join(os.getcwd(), demo.output_dir)
    graph_difference_absolute_path += '/Differences/'
    d.set_mounted_input_directory(graph_difference_absolute_path)

    absolute_output_dir = os.path.join(os.getcwd(), demo.output_dir)
    absolute_output_dir += '/TemporalTileset/'
    d.set_mounted_output_directory(absolute_output_dir)

    d.run()
