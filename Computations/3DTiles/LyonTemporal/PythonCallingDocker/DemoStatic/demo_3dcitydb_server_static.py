import os
import sys
import logging
from docker_3dcitydb_server import Docker3DCityDBServer
from demo_static import DemoWithDataBaseStatic


class Demo3dCityDBServerStatic(DemoWithDataBaseStatic):

    def __init__(self):
        super().__init__()
        super().__init_database__()
        self.active_database = None

    def get_database_dir(self, create=True):
        """
        The placeholder directory for database content in order for them to persist
        as files (persistence in the container being a little trickier)
        """
        postgres_output_path = os.path.join(os.getcwd(),
                                            self.get_output_dir(),
                                            'postgres-data-static')
        if create and not os.path.isdir(postgres_output_path):
            logging.info(f'Creating local output dir {postgres_output_path} in order '
                        f'to hold the postgres database content.')
            os.mkdir(postgres_output_path)
        return postgres_output_path

    def run(self):
        self.create_output_dir()   # Just making sure
        if self.active_database:
            logging.info('A database server already exists. Exiting')
            sys.exit(1)
        self.active_database = Docker3DCityDBServer.start_single_database(
            self.vintage,
            self.database, 
            self.get_database_dir())

    def halt(self):
        if not self.active_database:
            logging.info('No active database. Exiting')
            sys.exit(1)
        logging.info(f'Halting database container' 
                     f'{self.active_database.get_container().name}')
        self.active_database.halt_service()
        logging.info(f'Halting database container: done')
