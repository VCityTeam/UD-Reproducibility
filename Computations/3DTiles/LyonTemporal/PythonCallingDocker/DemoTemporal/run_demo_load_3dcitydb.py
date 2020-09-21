import os
import sys
import logging
import time
import demo_workflow_temporal as workflow

        
if __name__ == '__main__':
    load = workflow.demo_load
    load.create_output_dir()

    logger = logging.getLogger(__name__)
    log_filename = os.path.join(load.get_output_dir(), 'demo_load_3dcitydb.log')
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    logging.info('Stage 1: starting databases.')
    servers = workflow.demo_db_server
    # FIXME: for some unknown reason the following line makes things go
    # wrong. Inquire on this only if you wish to rename the output directory name.
    # servers.set_results_dir('data_bases')
    servers.run()
    logging.info('Stage 1: done.')

    logging.info('Stage 2: waiting an extra 2 minutes for databases to spin off.')
    time.sleep(120)
    logging.info('Stage 2: done.')

    logging.info('Stage 3: importing files to databases.')
    load.run()
    logging.info('Stage 3: done')

    logging.info('Stage 4: halting containers.')
    servers.halt()
    logging.info('Stage 4: done')

    logging.info('Stage 5: trivial (out of logs) testing of results.')
    if not load.check_log_result(log_filename):
        logging.info('Stage 5: failed.')
        sys.exit(1)
    logging.info('Stage 5: done')
