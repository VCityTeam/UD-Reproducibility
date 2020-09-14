import os
import sys
import logging
import shutil
from docker_temporal_tiler import DockerTemporalTiler
from demo import DemoWithDataBases


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
