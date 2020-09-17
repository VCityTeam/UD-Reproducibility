import os
import sys
import logging
from docker_3duse import Docker3DUse


class DockerSplitBuilding(Docker3DUse):

    def __init__(self):
        super().__init__()
        self.working_dir = '/root/3DUSE/Build/src/utils/cmdline/'
        self.input_filename = None
        self.output_filename = None
        self.command_output_directory = None

    def assert_ready_for_run(self):
        if not self.input_filename:
            logging.info('Missing input_filename for running. Exiting')
            sys.exit(1)
        if not self.output_filename:
            logging.info('Missing output_filename for running. Exiting')
            sys.exit(1)

    def set_input_filename(self, input_filename):
        full_input_filename = os.path.join(self.mounted_input_dir,
                                           input_filename)
        if not os.path.isfile(full_input_filename):
            logging.info(f'Input file {full_input_filename} not found. Exiting')
            sys.exit(1)
        self.input_filename = input_filename

    def set_output_filename(self, output_filename):
        self.output_filename = output_filename

    def set_command_output_directory(self, output_directory):
        # This is internal to the container and as seen by the container
        # command (as opposed to the directory mounted from "outside" the
        # container i.e. DockerHelperBase.mounted_output_dir)
        self.command_output_directory = output_directory

    def get_command(self):
        self.assert_ready_for_run()
        command = 'splitCityGMLBuildings '   # Mind the trailing separator
        command += '--input-file /Input/' + self.input_filename + ' '
        # In order to set the output the syntax of splitCityGMLBuildings
        # separates the directory from the file specifications:
        command += '--output-file ' + self.output_filename + ' '

        if self.mounted_input_dir == self.mounted_output_dir:
            # Because mounting twice the same directory will be avoided
            # in the DockerHelp.run() method.
            command += '--output-dir /Input/'
        else:
            command += '--output-dir /Output/'
        if self.command_output_directory:
            command += self.command_output_directory + ' '
        return command

    @staticmethod
    def split(input_dir, input_filename, output_filename):
        d = DockerSplitBuilding()
        # Docker only accepts absolute path names as argument for its volumes
        # to be mounted:
        absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)
        d.set_mounted_input_directory(absolute_path_input_dir)

        # Setting up, the output directory:
        #  1. side by side with input file: use
        #     d.set_mounted_output_directory(d.get_mounted_input_directory())
        #  2. in some arbitrary designated place: use e.g.
        #     output_dir = os.path.join(os.getcwd(),'some_dir')
        #     if not os.path.exists(output_dir):
        #         os.makedir(output_dir)
        #     d.set_mounted_output_directory(output_dir)
        #  3. in the invocation directory: just leave the output directory unset
        #
        # Optionally one can define the output directory to be a sub-directory
        # of the mounted output directory with
        # d.set_command_output_directory('LYON_1ER')
        #
        # For this example we chose option 1.
        d.set_mounted_output_directory(d.get_mounted_input_directory())
        d.set_input_filename(input_filename)
        d.set_output_filename(output_filename)
        logging.info(f'DockerSplitBuilding: spliting file '
                     f'{os.path.join(absolute_path_input_dir, input_filename)} '
                     f'to resulting file '
                     f'{os.path.join(absolute_path_input_dir, output_filename)}')
        d.run()
