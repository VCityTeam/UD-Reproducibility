import sys
import os
import logging
import time
import pytest

sys.path.insert(0, '.')
from docker_3dcitydb_server import Docker3DCityDBServer


class TestDocker3DCityDBServer:

    def shared(self):
        # We need to redirect DockerHelperBase loggers to standard output
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def test_docker_helper_service_start_and_halt(self):
        """
        Indirectly test DockerHelperService.halt_service() and thus the
        DockerHelperService class.
        """
        self.shared()

        container = Docker3DCityDBServer()
        configuration_file = 'DBConfigPyTest.yml'
        if not os.path.isfile(configuration_file):
            logging.info(f'Missing configuration file {configuration_file}.')
            configuration_file = 'DBConfig2009.yml'
            if not os.path.isfile(configuration_file):
                pytest.fail(f'Cannot fold back to configuration file '
                              f'{configuration_file}. Failing')

        container.set_config_file(configuration_file)
        container.load_config_file()
        container.run()

        logging.info('Sleeping for 10 seconds for container to spin up.')
        time.sleep(10)
        logging.info(f'Halting container {container.get_container().name}.')
        container.halt_service()



