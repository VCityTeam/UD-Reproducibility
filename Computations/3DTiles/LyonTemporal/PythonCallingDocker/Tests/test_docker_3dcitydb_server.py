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

    # Note: in the future this will be named start_docker_.. and be called by
    # the tiler test. In addition, the part halting the server should be
    # moved to another method of this class and called by the tiler test at
    # the end. To this end, we should make an active_databases[] class
    # attribute.
    @pytest.mark.run(order=6)
    def test_docker_3dcitydb_server_lyon_1er_2009_2012(self):
        self.shared()

        vintages = ['2009', '2012']

        for vintage in vintages:
            container = Docker3DCityDBServer()
            configuration_file = 'DBConfig' + vintage + '.yml'
            if not os.path.isfile(configuration_file):
                logging.info(
                    f'Missing configuration file {configuration_file}.')

            container.set_config_file(configuration_file)
            container.load_config_file()
            container.run()

            logging.info('Sleeping for 10 seconds for container to spin up.')
            time.sleep(10)
            logging.info(f'Halting container {container.get_container().name}.')
            container.halt_service()
