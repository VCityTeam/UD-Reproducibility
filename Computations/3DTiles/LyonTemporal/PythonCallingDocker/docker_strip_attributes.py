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


def strip_single_file(container,
                      input_dir,
                      input_filename,
                      output_filename,
                      output_dir=None):
    """
    A function to be used to manually handle the stripping of a single file
    (basicallyt a wrap of the container invocation)
    :param container: a DockerStripAttributes instance
    :param input_dir: the directory where the input file is to be found
    :param input_filename: the name of the input file
    :param output_filename: the name of the output file
    :param output_dir: the directory where the output file is to be placed.
                       When invocation ommits the output_dir, this function
                       places its result in the input_dir
    :return: the resulting output filename
    """

    # Docker only accepts absolute path names as argument for its volumes
    # to be mounted:
    absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)

    container.set_mounted_input_directory(absolute_path_input_dir)
    container.set_mounted_output_directory(
        container.get_mounted_input_directory())
    container.set_input_filename(input_filename)
    container.set_output_filename(output_filename)
    container.run()

    full_output_filename = os.path.join(input_dir, output_filename)
    logging.info(f'Striping to yield file {full_output_filename}.')
    if not os.path.isfile(full_output_filename):
        logging.error(
            f'Output file {full_output_filename} not found. Exiting.')
        sys.exit(1)

    if not output_dir:
        return full_output_filename
    else:
        # Since CityGML2Stripper does not allow to specify an output folder,
        # we need to "manually" move the resulting file
        target_filename = os.path.join(output_dir, output_filename)
        logging.info(f'Moving resulting file from {full_output_filename} ')
        logging.info(f'to {target_filename}.')
        os.replace(full_output_filename, target_filename)
        return target_filename

