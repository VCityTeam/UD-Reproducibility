import os
import sys
import logging
from docker_tiler_base import DockerTilerBase


class DockerTilerTemporal(DockerTilerBase):
    def __init__(self):
        super().__init__()
        self.vintages = list()

    def assert_ready_for_run(self):
        super().assert_ready_for_run()
        if not self.vintages:
            logging.info('Missing vintages for running. Please specify at '
                         'least two vintages.')
            sys.exit(1)
        if len(self.db_config_filenames) != len(self.vintages):
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

    def set_db_config_filenames(self, db_config_files):
        if not isinstance(db_config_files, list):
            logging.info('set_db_config_files() waits for a list of vintages.')
            sys.exit(1)
        if len(db_config_files) < 2:
            logging.info('You must provide at list two database configuration '
                         'files.')
            sys.exit(1)
        self.db_config_filenames = db_config_files

    def get_command(self):
        self.assert_ready_for_run()
        # The Tiler to run, see ../Docker/CityTiler-DockerContext/entrypoint.py
        command = 'TemporalTiler '
        command += '--db_config_path '
        for db_config in self.db_config_filenames:
            command += '/Input/' + db_config + ' '
        command += '--time_stamp '
        for vintage in self.vintages:
            command += str(vintage) + ' '
        return command

