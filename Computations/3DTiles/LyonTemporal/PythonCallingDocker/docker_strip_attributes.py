import os
import sys
import logging
from docker_helper import DockerHelperBase
import demo_configuration as demo


class DockerStripAttributes(DockerHelperBase):

    def __init__(self):
        super().__init__('liris:CityGML2Stripper')
        context_dir = os.path.join(os.getcwd(),
                                   '..',
                                   'Docker',
                                   'CityGML2Stripper-DockerContext')
        self.build(context_dir)

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

        if self.mounted_input_dir == self.mounted_output_dir:
            # Because mounting twice the same directory will be avoided
            # in the DockerHelp.run() method.
            command += '--output /Input/'
        else:
            command += '--output /Output/'
        command += self.output_filename + ' '
        return command


def strip(input_dir, input_filename, output_filename):
    d = DockerStripAttributes()

    # Docker only accepts absolute path names as argument for its volumes
    # to be mounted:
    absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)

    d.set_mounted_input_directory(absolute_path_input_dir)
    d.set_mounted_output_directory(d.get_mounted_input_directory())
    d.set_input_filename(input_filename)
    d.set_output_filename(output_filename)

    d.run()

    # Since CityGML2Stripper does not allow to specify an output folder,
    # you can use os.replace to move the resulting file to a specific folder.
    # For instance, you can do:
    #   os.replace('LYON_1ER_BATI_2009_splited_stripped.gml',
    #              '/path/to/destination/folder/LYON_1ER_BATI_2009_splited_stripped.gml')


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Note: there is probably something simpler to be done with
    # LyonMetropoleDowloadAndSanitize.get_resulting_filenanes() but we
    # cannot access it in this context
    inputs = list()
    for borough in demo.boroughs:
        for vintage in demo.vintages:
            inputs.append(
                [os.path.join(demo.output_dir, borough + '_' + str(vintage)),
                 borough + '_BATI_' + str(vintage) + '_splited.gml',
                 borough + '_BATI_' + str(vintage) + '_splited_stripped.gml'])

    for f in inputs:
        print("Now handling", f)
        strip(input_dir=f[0], input_filename=f[1], output_filename=f[2])