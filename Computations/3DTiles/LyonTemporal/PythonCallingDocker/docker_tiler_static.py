import os
import sys
import logging
from docker_tiler_base import DockerTilerBase


class DockerTilerStatic(DockerTilerBase):
    def __init__(self):
        super().__init__()

    def assert_ready_for_run(self):
        super().assert_ready_for_run()
        if len(self.db_config_filenames) != 1:
            logging.info('DockerTilerStatic expects a single database configuration ')
            sys.exit(1)

    def get_command(self):
        self.assert_ready_for_run()
        # The Tiler to run, see ../Docker/CityTiler-DockerContext/entrypoint.py
        command = 'Tiler '
        db_config = self.db_config_filenames[0]
        command += '/Input/' + db_config + ' '
        logging.info('Command launch : ' + command)
        return command
