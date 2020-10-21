import os
import sys
import logging
import docker
from docker_helper import DockerHelperPull, DockerHelperService


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

        self.container_name = db_config['PG_NAME']

    def get_command(self):
        # No command is declared here since the command is already set
        # by default in the Dockerfile
        return None

    def run(self):
        """
        Overloads the run method of DockerHelperService.
        :return:
        """
        self.add_volume(self.get_mounted_output_directory(),
                        '/var/lib/postgresql/data',
                        'rw')
        super().run()

    def halt_service(self):
        # We cannot rely on the configuration (at Dockerfile level) realized by the
        # packagers ("containerization") of the database service. In particular we
        # don't know
        #  * if they chose to send a signal to the database server and, when they
        #    did, what signal they did chose (chosen shutdown method is "smart", 
        #    "fast" or "immediate", refer to
        #    https://www.postgresql.org/docs/12/app-pg-ctl.html
        #  * when the container receives the 'stop signal will it expect long 
        #   enough for the database to realize it shutdown ?
        # At the application level one thus needs to explictly require the 
        # database to realize its snapshot and then shutdown.
        # The following implements the equivalent of the following CLI command
        #    `docker exec <container-id> pg_ctl stop -m fast`...
        try:
            logging.info(f'Within container {self.container_name}, requesting '
                          'the database for a clean snapshot (push its commits '
                          'into its tables and clear its logs).')
            trace = self.get_container().exec_run(
                cmd=['pg_ctl', 'stop', '-m', 'fast'],
                user='postgres')
            logging.info(f'Database snaphot looks good [{trace}].')
        except docker.errors.APIError:
            logging.error('Database snapshot probably failed. Expect some really'
                          'long delays on next starting...')

        super().halt_service()

    @staticmethod
    def start_single_database(db_vintage, db_config, postgres_data_output_path):
        data_base = Docker3DCityDBServer(db_vintage, db_config)
        absolute_path_output_dir = os.path.join(postgres_data_output_path,
                                                data_base.container_name)
        if not os.path.isdir(absolute_path_output_dir):
            logging.info(f'Creating directory {absolute_path_output_dir} to '
                        f'store postgres database content for vintage {db_vintage}.')
            os.mkdir(absolute_path_output_dir)
        data_base.set_mounted_output_directory(absolute_path_output_dir)
        data_base.run()
        logging.info(f'3DCityDB server container of database {data_base.container_name} '
                     f'(for vintage {db_vintage}) started.')
        return data_base

