import os
import sys
import logging
import time
import demo_workflow_temporal as workflow


if __name__ == '__main__':
    demo_servers = workflow.demo_db_server
    demo_servers.create_output_dir()

    logger = logging.getLogger(__name__)
    log_filename = os.path.join(demo_servers.get_output_dir(),
                                'demo_3dcitydb_server.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    demo_servers.run()
    logging.info('Enjoying the databases hum for 2 minutes.')
    time.sleep(120)
    demo_servers.halt()
