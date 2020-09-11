import os
import sys
import logging
import time
import shutil
from docker_temporal_tiler import DockerTemporalTiler
from demo_3dcitydb_server import Demo3dCityDBServer
from demo import DemoWithDataBases
import demo_full_workflow as workflow


class DemoTemporalTiler(DemoWithDataBases):

    def __init__(self):
        super().__init__()
        super().__init_databases__()

    def run(self):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("DemoTemporalTiler misses some of its input files: exiting")
            sys.exit(1)
        
        container = DockerTemporalTiler()
        container.set_vintages(self.vintages)

        # ### Prepare the input directory and its content (the inputs should be located
        # into a single directory that the container will mount).
        # FIXME: this copy logic belongs to the DockerTemporalTiler class and not here.
        # FIXME: the container can only mount absolute pathname directories. But do we
        #        need to propagate this container constraint to the caller's invocation ?
        input_dir = os.path.abspath(os.path.join(self.get_output_dir(), 'InputFiles'))
        if not os.path.isdir(input_dir):
            logging.info(f'Creating local input directory {input_dir} in order to '
                        f'hold differences files.')
            os.makedirs(input_dir)
        container.set_mounted_input_directory(input_dir)

        # Generate the database configuration files.
        db_config_file_basenames = list()
        for vintage in self.vintages:
            config_filename = os.path.join(input_dir, 
                                          'CityTilerDBConfig' + str(vintage) + '.yml')
            container.generate_configuration_file(vintage,
                                                  self.databases[vintage],
                                                  config_filename)
            db_config_file_basenames.append(os.path.basename(config_filename))
        # And inform the container of those configuration filenames                                
        container.set_db_config_filenames(db_config_file_basenames)

        # Proceed with copying the difference files to the input directory.
        for file in input.get_resulting_filenames():
            shutil.copy(file, input_dir)

        output_dir = os.path.abspath(os.path.join(self.get_output_dir(), 'TemporalTileset'))
        if not os.path.isdir(output_dir):
            logging.info(f'Creating local output dir {output_dir} for '
                        f'the resulting tileset.')
            os.makedirs(output_dir)
        container.set_mounted_output_directory(output_dir)

        container.run()


if __name__ == '__main__':
    temporal_tiler = workflow.demo_tiler
    temporal_tiler.create_output_dir()

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.join(temporal_tiler.get_output_dir(),
                                              'demo_temporal_tiler.log'),
                        filemode='w')

    logging.info('Stage 1: start databases wait.')
    demo_servers = Demo3dCityDBServer()
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


