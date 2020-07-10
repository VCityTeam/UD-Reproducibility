import os
import sys
import logging
import yaml
import time

from docker_helper import DockerHelper
import demo_configuration as demo

# This class misses a stop() or halt() method
class Docker3DCityDBServer(DockerHelper):

    def __init__(self):
        super().__init__('tumgis/3dcitydb-postgis')
        # FIXME: The tag should be an attribute of the
        #  to be created DockerBuild (or DockerHelperBuild)
        self.pull('v4.0.2')

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
                print('ERROR: ', sys.exec_info()[0])
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
            print('ERROR: Database is not properly defined in ' + self.config_file + ', please refer to README.md')
            sys.exit(1)

        self.environment = {'CITYDBNAME': db_config['PG_NAME'],
                            'SRID': 3946,
                            'SRSNAME': 'espg:3946',
                            'POSTGRES_USER': db_config['PG_USER'],
                            'POSTGRES_PASSWORD': db_config['PG_PASSWORD']}

        self.ports = {'5432/tcp':db_config['PG_PORT']}
        self.vintage = db_config['PG_VINTAGE']

        self.config_file_loaded = True

    def assert_ready_for_run(self):
        if not self.config_file:
            logging.info('Missing config_file for running. Exiting')
            sys.exit(1)
        if not self.config_file_loaded:
            logging.info('Config file not loaded. Exiting')
            sys.exit(1)

    def get_command(self):
        # No command is declared here since we pull this docker from the registry
        return None


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='docker_3dcitydb_server.log',
                        filemode='w')

    active_databases = list()
    for i, vintage in enumerate(demo.vintages):
        print('Starting database for the ', vintage, ' vintage.')
        active_databases.append(Docker3DCityDBServer())
        active_databases[i].set_config_file('DBConfig' + str(vintage) + '.yml')
        active_databases[i].load_config_file()
        active_databases[i].run_service()
