import sys
import logging
import time
import os
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

        # This test may be launched alone. We need to make sure the output
        # directory has been created.
        pytest_output_path = os.path.join(os.getcwd(), 'pytest_outputs')
        if not os.path.isdir(pytest_output_path):
            os.mkdir(pytest_output_path)
        # Create another directory in pytest_outputs for the postgres-data
        postgres_output_path = os.path.join(pytest_output_path,
                                            'postgres-data')
        if not os.path.isdir(postgres_output_path):
            os.mkdir(postgres_output_path)

        vintages = [2009, 2012]
        # FIXME: we should probably have a test_configuration.py (similarly
        #  to demo_configuration.py) for that...
        databases_config = {
            2009: {
                'PG_HOST': '192.168.1.51',
                'PG_PORT': '5432',
                'PG_NAME': 'citydb-full_lyon-2009',
                'PG_USER': 'postgres',
                'PG_PASSWORD': 'postgres'
            },
            2012: {
                'PG_HOST': '192.168.1.51',
                'PG_PORT': '5433',
                'PG_NAME': 'citydb-full_lyon-2012',
                'PG_USER': 'postgres',
                'PG_PASSWORD': 'postgres'
            }
        }

        for vintage in vintages:
            container = Docker3DCityDBServer(vintage, databases_config[vintage])
            absolute_path_output_dir = os.path.join(postgres_output_path,
                                                    container.container_name)
            if not os.path.isdir(absolute_path_output_dir):
                os.mkdir(absolute_path_output_dir)
            container.set_mounted_output_directory(absolute_path_output_dir)
            container.run()

            logging.info('Sleeping for 10 seconds for container to spin up.')
            time.sleep(10)
            logging.info(f'Halting container {container.get_container().name}.')
            container.halt_service()
