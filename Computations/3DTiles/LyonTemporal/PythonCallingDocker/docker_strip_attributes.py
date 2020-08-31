import os
import sys
import logging
from docker_helper import DockerHelperBuild, DockerHelperTask


class DockerStripAttributes(DockerHelperBuild, DockerHelperTask):

    def __init__(self):
        super().__init__('liris', 'CityGML2Stripper')
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
        # We don't need to specify the executable since an entrypoint
        # is specified in the DockerFile of DockerStripAttributes
        command = '--input /Input/' + self.input_filename + ' '

        if self.mounted_input_dir == self.mounted_output_dir:
            # Because mounting twice the same directory will be avoided
            # in the DockerHelp.run() method.
            command += '--output /Input/'
        else:
            command += '--output /Output/'
        command += self.output_filename + ' '
        return command

    def run(self):
        # Set input and output volumes
        self.add_volume(self.mounted_input_dir, '/Input', 'rw')
        if not self.mounted_input_dir == self.mounted_output_dir:
            # When mounting the same directory twice (which is the case when
            # the input and output directory are the same) then containers.run()
            # raises a docker.errors.ContainerError. Hence we only mount the
            # /Output volume when they both differ. Note that when this
            # happens the command in the derived class must be altered in order
            # to place its output in the /Input mounted point (because in this
            # /Output is (equal to) /Input.
            self.add_volume(self.mounted_output_dir, '/Output', 'rw')
        super().run()


