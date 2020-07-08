import os
import sys
import logging
from docker_helper import DockerHelper


class DockerStripAttributes(DockerHelper):

    def __init__(self):
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   'CityGML2Stripper-DockerContext')
        tag_name = 'liris:CityGML2Stripper'
        super().__init__(context_dir, tag_name)
        self.working_dir = '/root/UD-Serv/Utils/CityGML2Stripper'
        self.input_filename = None
        self.output_filename = None

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

    def get_command(self):
        self.assert_ready_for_run()
        # We don't need to specify the executable since an entrypoint is specified in the DockerFile of
        # DockerStripAttributes
        command = '--input /Input/' + self.input_filename + ' '
        command += '--output /Output/' + self.output_filename + ' '
        return command


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='docker_strip_attributes.log',
                        filemode='w')

    d = DockerStripAttributes()

    input_directory = os.path.join(os.getcwd(), 'junk/LYON_1ER_2009')
    d.set_mounted_input_directory(input_directory)
    d.set_input_filename('LYON_1ER_BATI_2009_splited.gml')
    d.set_output_filename('LYON_1ER_BATI_2009_splited_stripped.gml')

    d.run()

    # Since CityGML2Stripper does not allow to specify an output folder,
    # you can use os.replace to move the resulting file to a specific folder.
    # For instance, you can do:
    #   os.replace('LYON_1ER_BATI_2009_splited_stripped.gml',
    #              '/path/to/destination/folder/LYON_1ER_BATI_2009_splited_stripped.gml')
