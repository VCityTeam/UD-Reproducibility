import os
import sys
import logging
import time

from docker_helper import DockerHelperPull, DockerHelperService
import demo_configuration as demo


class Docker3DCityDBServer(DockerHelperPull, DockerHelperService):

    def __init__(self, db_vintage, db_config):
        super().__init__('tumgis/3dcitydb-postgis', 'v4.0.2')
        self.pull()

        # Check that db configuration is well defined
        if (('PG_HOST' not in db_config)
                or ('PG_USER' not in db_config)
                or ('PG_PORT' not in db_config)
                or ('PG_NAME' not in db_config)
                or ('PG_USER' not in db_config)
                or ('PG_PASSWORD' not in db_config)):
            logging.error('Database is not properly defined in ' +
                          self.config_file + ', please refer to README.md')
            sys.exit(1)

        self.vintage = db_vintage
        self.db_config = db_config
        # ports hold the mapping between internal and external ports
        # of the container as it will be passed to the run method of
        # docker sdk
        self.ports = {'5432/tcp': db_config['PG_PORT']}
        self.environment = {'CITYDBNAME': db_config['PG_NAME'],
                            'SRID': 3946,
                            'SRSNAME': 'espg:3946',
                            'POSTGRES_USER': db_config['PG_USER'],
                            'POSTGRES_PASSWORD': db_config['PG_PASSWORD']}

        self.container_name = 'citydb-container-' + str(self.vintage)

    def get_command(self):
        # No command is declared here since the command is already set
        # by default in the Dockerfile
        return None

    def run(self):
        """
        Overloads the run method of DockerHelperService.
        :return:
        """
        absolute_path_output_dir = os.path.join(os.getcwd(),
                                                demo.output_dir,
                                                'postgres-data',
                                                self.container_name)
        if not os.path.isdir(absolute_path_output_dir):
            logging.info('Creating local mount-point directory '
                         f'{absolute_path_output_dir}')
            os.mkdir(absolute_path_output_dir)

        self.add_volume(absolute_path_output_dir,
                        '/var/lib/postgresql/data',
                        'rw')
        super().run()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    active_databases = list()
    for vintage in demo.vintages:
        if not demo.databases:
            logging.info(f'Databases configurations not found. Exiting')
            sys.exit(1)
        if not demo.databases[vintage]:
            logging.info(f'Database configuration for vintage {vintage} not '
                         f'found. You must specify one database configuration '
                         f'per vintage. Exiting')
            sys.exit(1)
        data_base = Docker3DCityDBServer(vintage, demo.databases[vintage])
        data_base.run()
        active_databases.append(data_base)

    logging.info('Enjoying the databases hum for 10 seconds.')
    time.sleep(10)

    logging.info(f'Halting containers: begining')
    for server in active_databases:
        logging.info(f'   Halting container {server.get_container().name}.')
        server.halt_service()
    logging.info(f'Halting containers: done')
