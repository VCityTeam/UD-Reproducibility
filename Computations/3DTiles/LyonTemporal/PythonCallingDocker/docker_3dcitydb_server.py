import os
import sys
import logging
import yaml

from docker_helper import DockerHelper
import demo_configuration as demo


class Docker3DCityDBServer(DockerHelper):

    def __init__(self):
        super().__init__('tumgis/3dcitydb-postgis')
        self.pull()

        self.config_file = None
        self.config_file_loaded = False

        # Defined in config_file
        self.PG_HOST = None
        self.PG_PORT = None
        self.PG_NAME = None
        self.PG_USER = None
        self.PG_PASSWORD = None
        self.PG_VINTAGE = None

    def set_config_file(self, config_file):
        if not os.path.isfile(config_file):
            logging.info(f'Input file {config_file} not found.'
                         ' Exiting')
            sys.exit(1)
        self.config_file = config_file

    def load_config_file(self):
        self.config_file = config_file
        with open(config_file, 'r') as db_config_file:
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
            print('ERROR: Database is not properly defined in ' + config_file + ', please refer to README.md')
            sys.exit(1)

        self.PG_HOST = db_config['PG_HOST']
        self.PG_PORT = db_config['PG_PORT']
        self.PG_NAME = db_config['PG_NAME']
        self.PG_USER = db_config['PG_USER']
        self.PG_PASSWORD = db_config['PG_PASSWORD']
        self.PG_VINTAGE = db_config['PG_VINTAGE']

        self.config_file_loaded = True

    def assert_ready_for_run(self):
        if not self.config_file:
            logging.info('Missing config_file for running. Exiting')
            sys.exit(1)
        if not self.config_file_loaded:
            logging.info('Config file not loaded. Exiting')
            sys.exit(1)

    def get_command(self):
        self.assert_ready_for_run()
        # FIXME: There is double quotes in the docker run of LaunchDataBaseSingleServer.sh.j2
        # Are those needed ?
        command = '--rm -dt --name citydb-container-' + self.PG_VINTAGE + ' '
        command += '-p ' + self.PG_PORT + ':5432 '
        command += '-e CITYDBNAME=' + self.PG_NAME + ' '
        command += '-e SRID=3946 '
        command += '-e SRSNAME=espg:3946 '
        command += '-e POSTGRES_USER=' + self.PG_USER + ' '
        command += '-e POSTGRES_PASSWORD=' + self.PG_PASSWORD + ' '
        command += 'tumgis/3dcitydb-postgis '


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
        active_databases.set_config_file('DBConfig' + vintage + '.yml')
        active_databases[i].load_config_file()
        active_databases[i].run()