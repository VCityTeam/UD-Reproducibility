import os
import sys
import logging
import shutil

from demo_static import DemoWithDataBaseStatic
from docker_tiler_static import DockerTilerStatic


class DemoTilerStatic(DemoWithDataBaseStatic):

    def __init__(self):
        super().__init__()
        super().__init_database__()

    def run(self):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("DemoTemporalTiler misses some of its input files: exiting")
            sys.exit(1)
        
        container = DockerTilerStatic()

        # ### Prepare the input directory and its content (the inputs should be located
        # into a single directory that the container will mount).
        input_dir = os.path.abspath(os.path.join(self.get_output_dir(), 'InputFiles'))
        if not os.path.isdir(input_dir):
            logging.info(f'Creating local input directory {input_dir} in order to '
                         f'hold database configuration file.')
            os.makedirs(input_dir)
        container.set_mounted_input_directory(input_dir)

        # Generate the database configuratio file
        db_config_filename = os.path.join(
            input_dir, 
            'CityTilerDBConfigStatic' + str(self.vintage) + '.yml')
        container.generate_configuration_file(self.vintage,
                                              self.database,
                                              db_config_filename)
        # Inform the container of such configuration filename                                
        container.add_db_config_filename(os.path.basename(db_config_filename))

        output_dir = os.path.abspath(self.get_output_dir())
        if not os.path.isdir(output_dir):
            logging.info(f'Creating local output dir {output_dir} for '
                        f'the resulting tileset.')
            os.makedirs(output_dir)
        container.set_mounted_output_directory(output_dir)

        container.run()
