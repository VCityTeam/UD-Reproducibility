import os
import sys
import logging
from docker_3duse import Docker3DUse
import demo_configuration as demo


class DockerExtractBuildingDates(Docker3DUse):

    def __init__(self):
        super().__init__()
        self.working_dir = '/root/3DUSE/Build/src/utils/cmdline/'
        self.first_date = None
        self.second_date = None
        self.first_input_filename = None
        self.second_input_filename = None
        self.command_output_directory = None

    def assert_ready_for_run(self):
        if not self.first_date:
            logging.info('Missing first_date for running. Exiting')
            sys.exit(1)
        if not self.second_date:
            logging.info('Missing second_date for running. Exiting')
            sys.exit(1)
        if not self.first_input_filename:
            logging.info('Missing first_input_filename for running. Exiting')
            sys.exit(1)
        if not self.second_input_filename:
            logging.info('Missing second_input_filename for running. Exiting')
            sys.exit(1)

    def set_first_date(self, date):
        self.first_date = date

    def set_second_date(self, date):
        self.second_date = date

    def set_first_input_filename(self, first_input_filename):
        full_first_input_filename = os.path.join(self.mounted_input_dir,
                                                 first_input_filename)
        if not os.path.isfile(full_first_input_filename):
            logging.info(f'Input file {full_first_input_filename} not found.'
                         ' Exiting')
            sys.exit(1)
        self.first_input_filename = first_input_filename

    def set_second_input_filename(self, second_input_filename):
        full_second_input_filename = os.path.join(self.mounted_input_dir,
                                                  second_input_filename)
        if not os.path.isfile(full_second_input_filename):
            logging.info(f'Input file {full_second_input_filename} not found.'
                         ' Exiting')
            sys.exit(1)
        self.second_input_filename = second_input_filename

    def set_command_output_directory(self, output_directory):
        # This is internal to the container and as seen by the container
        # command (as opposed to the directory mounted from "outside" the
        # container i.e. DockerHelperBase.mounted_output_dir)
        self.command_output_directory = output_directory

    def get_command(self):
        self.assert_ready_for_run()
        command = 'extractBuildingDates '  # Mind the trailing separator

        command += '--first_date ' + self.first_date + ' '
        command += '--first_file /Input/' + self.first_input_filename + ' '

        command += '--second_date ' + self.second_date + ' '
        command += '--second_file /Input/' + self.second_input_filename + ' '

        if self.mounted_input_dir == self.mounted_output_dir:
            # Because mounting twice the same directory will be avoided
            # in the DockerHelp.run() method.
            command += '--output_dir /Input/'
        else:
            command += '--output_dir /Output/'
        if self.command_output_directory:
            command += self.command_output_directory + ' '
        return command

    @staticmethod
    def single_extract(first_date,
                    first_input_filename,
                    second_date,
                    second_input_filename,
                    output_dir):
        d = DockerExtractBuildingDates()
        # Docker only accepts absolute path names as argument for its volumes
        # to be mounted:
        absolute_path_input_dir = os.path.join(os.getcwd())
        d.set_mounted_input_directory(absolute_path_input_dir)
        d.set_mounted_output_directory(d.get_mounted_input_directory())

        d.set_first_date(first_date)
        d.set_first_input_filename(first_input_filename)
        d.set_second_date(second_date)
        d.set_second_input_filename(second_input_filename)
        d.set_command_output_directory(output_dir)

        d.run()

