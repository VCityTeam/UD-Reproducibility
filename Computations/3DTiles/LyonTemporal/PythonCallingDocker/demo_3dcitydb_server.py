import os
import sys
import logging
import time

from docker_3dcitydb_server import Docker3DCityDBServer
import demo_configuration as demo


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    active_databases = list()
    for vintage in demo.vintages:
        if not demo.databases:
            logging.info(f'Databases configurations not found. Exiting')
            sys.exit(1)
        if not demo.databases[vintage]:
            logging.info(f'Database configuration for vintage {vintage} was not '
                        f'found. You must specify one database configuration '
                        f'per vintage. Exiting')
            sys.exit(1)
        db_config = demo.databases[vintage]

        # Setup a placeholder for database contents in order for them to stand
        # outside the container    
        postgres_output_path = os.path.join(os.getcwd(),
                                            demo.output_dir,
                                            'postgres-data')
        if not os.path.isdir(postgres_output_path):
            logging.info(f'Creating local output dir {postgres_output_path} in order '
                        f'to hold the various postgres databases contents.')
            os.mkdir(postgres_output_path)
    
        vintaged_db = Docker3DCityDBServer.start_single_database(vintage,
                                                                 db_config, 
                                                                 postgres_output_path)
        active_databases.append(vintaged_db)

    logging.info('Enjoying the databases hum for 10 seconds.')
    time.sleep(10)

    logging.info(f'Halting containers: begining')
    for server in active_databases:
        logging.info(f'   Halting container {server.get_container().name}.')
        server.halt_service()
    logging.info(f'Halting containers: done')
