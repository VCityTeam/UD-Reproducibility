import os
import logging
import time
import demo_workflow_temporal as workflow


if __name__ == '__main__':
    temporal_tiler = workflow.demo_tiler
    temporal_tiler.create_output_dir()

    logger = logging.getLogger(__name__)
    log_filename = os.path.join(temporal_tiler.get_output_dir(),
                               'demo_tiler_temporal.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    logging.info('Stage 1: start databases wait.')
    demo_servers = workflow.demo_db_server
    demo_servers.run()
    logging.info('Stage 1: wait for 2 minutes for databases to spin off.')
    time.sleep(120)
    logging.info('Stage 1: done.')

    logging.info('Stage 2: computing the tiles.')
    temporal_tiler.run()
    logging.info('Stage 2: done.')

    logging.info('Stage 3: halting containers.')
    demo_servers.halt()
    logging.info('Stage 3: done')


