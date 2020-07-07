import os
import sys
import logging
from docker_helper import DockerHelper


class Docker3DUse(DockerHelper):

    def __init__(self):
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   '3DUse-DockerContext')
        tag_name = 'liris:3DUse'
        super().__init__(context_dir, tag_name)


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
        # container i.e. DockerHelper.mounted_output_dir)
        self.command_output_directory = output_directory

    def get_command(self):
        self.assert_ready_for_run()
        command = 'splitCityGMLBuildings '   # Mind the trailing separator
        command += '--input-file /Input/' + self.input_filename + ' '
        # In order to set the output the syntax of splitCityGMLBuildings
        # separates the directory from the file specifications:
        command += '--output-file ' + self.output_filename + ' '
        if not self.mounted_input_dir == self.mounted_output_dir:
            command += '--output-dir /Output/'
        else:
            command += '--output-dir /Input/'
        if self.command_output_directory:
            command += self.command_output_directory + ' '
        command += ' > DockerCommandOutput.log 2>&1'
        return command


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='docker_helper.log',
                        filemode='w')

    d = DockerSplitBuilding()
    d.set_mounted_input_directory(os.path.join(os.getcwd(),
                                               'junk/LYON_1ER_2009'))
    d.set_input_filename('LYON_1ER_BATI_2009.gml')
    output_dir = os.path.join(os.getcwd(),'junk_split')
    # output_dir = os.path.join(os.getcwd(), 'junk/LYON_1ER_2009')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    d.set_mounted_output_directory(output_dir)
    d.set_output_filename('LYON_1ER_BATI_2009_splited.gml')
    # Not strictly required d.set_command_output_directory('LYON_1ER')
    d.run()
