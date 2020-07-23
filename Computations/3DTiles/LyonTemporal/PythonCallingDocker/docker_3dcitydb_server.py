import os
import sys
import logging
import yaml
import time

from docker_helper import DockerHelperPull, DockerHelperService
import demo_configuration as demo


class Docker3DCityDBServer(DockerHelperPull, DockerHelperService):

    def __init__(self):
        super().__init__('tumgis/3dcitydb-postgis', 'v4.0.2')
        self.pull()

        self.config_file = None
        self.config_file_loaded = False

        # Defined in config_file
        # ports hold the mapping between internal and external ports
        # of the container as it will be passed to the run method of
        # docker sdk
        self.ports = None
        self.vintage = None
        self.environment = None

    def set_config_file(self, config_file):
        if not os.path.isfile(config_file):
            logging.info(f'Input file {config_file} not found.'
                         ' Exiting')
            sys.exit(1)
        self.config_file = config_file

    def load_config_file(self):
        with open(self.config_file, 'r') as db_config_file:
            try:
                db_config = yaml.load(db_config_file, Loader=yaml.FullLoader)
                db_config_file.close()
            except:
                logging.error(f'{sys.exec_info()[0]}. Exiting')
                db_config_file.close()
                sys.exit(1)

        # Check that db configuration is well defined
        if (('PG_HOST' not in db_config)
                or ('PG_USER' not in db_config)
                or ('PG_PORT' not in db_config)
                or ('PG_NAME' not in db_config)
                or ('PG_USER' not in db_config)
                or ('PG_PASSWORD' not in db_config)
                or ('PG_VINTAGE' not in db_config)):
            logging.error('Database is not properly defined in ' +
                          self.config_file + ', please refer to README.md')
            sys.exit(1)

        self.environment = {'CITYDBNAME': db_config['PG_NAME'],
                            'SRID': 3946,
                            'SRSNAME': 'espg:3946',
                            'POSTGRES_USER': db_config['PG_USER'],
                            'POSTGRES_PASSWORD': db_config['PG_PASSWORD']}

        self.ports = {'5432/tcp': db_config['PG_PORT']}
        self.vintage = db_config['PG_VINTAGE']
        self.container_name = 'citydb-container-' + str(self.vintage)

        self.config_file_loaded = True

    def assert_ready_for_run(self):
        if not self.config_file:
            logging.info('Missing config_file for running. Exiting')
            sys.exit(1)
        if not self.config_file_loaded:
            logging.info('Config file not loaded. Exiting')
            sys.exit(1)

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
                                                'postgres-data')
        if not os.path.isdir(absolute_path_output_dir):
            logging.info('Creating local mount-point directory '
                         f'{absolute_path_output_dir}')
            os.mkdir(absolute_path_output_dir)
        # FIXME: the class user must be able to specify the local directory
        # (we need to separate the vintage databases).

        self.add_volume(absolute_path_output_dir,
                        '/var/lib/postgresql/data',
                        'rw')
        super().run()


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    active_databases = list()
    for vintage in demo.vintages:
        data_base = Docker3DCityDBServer()
        data_base.set_config_file('DBConfig' + str(vintage) + '.yml')
        data_base.load_config_file()
        data_base.run()
        active_databases.append(data_base)

    logging.info('Enjoying the databases hum for 10 seconds.')
    time.sleep(10)

    logging.info(f'Halting containers: begining')
    for server in active_databases:
        logging.info(f'   Halting container {server.get_container().name}.')
        server.halt_service()
    logging.info(f'Halting containers: done')
