import os
import sys
import logging
from docker_helper import DockerHelperBuild, DockerHelperTask


class DockerXML2RDF(DockerHelperBuild, DockerHelperTask):

    def __init__(self):
        super().__init__('liris/ud-graph', 'latest')
        this_file_dir = os.path.dirname(os.path.realpath(__file__))
        context_dir = os.path.join(this_file_dir,
                                   'UD-Graph-DockerContext')
        self.build(context_dir)
        self.local_input_dir = '/home/user/UD-Graph/Transformations/input/'
        self.local_output_dir = '/home/user/UD-Graph/Transformations/output/'
        self.input_filename = None

    def assert_ready_for_run(self):
        if len(os.listdir(self.mounted_input_dir)) == 0:
            logging.error('Input directory is empty. Exiting')
            sys.exit(1)
        if self.input_filename is None:
            logging.error('Missing input_filename for running. Exiting')
            sys.exit(1)

    def set_input_filename(self, input_filename):
        full_input_filename = os.path.join(self.mounted_input_dir,
                                           input_filename)
        if not os.path.isfile(full_input_filename):
            logging.error(f'Input file {full_input_filename} not found. Exiting')
            sys.exit(1)
        self.input_filename = f'{self.local_input_dir}/{input_filename}'

    def get_command(self):
        self.assert_ready_for_run()
        # We don't need to specify the executable since an entrypoint
        # is specified in the DockerFile
        command = f'xml2rdf --model {self.local_input_dir} '
        command +=        f'--input {self.input_filename} '
        command +=        f'--output {self.local_output_dir} '
        # logging.info(f'command: {command}')
        return command

    def run(self):
        # Set input and output volumes
        self.add_volume(self.mounted_input_dir, self.local_input_dir, 'rw')
        self.add_volume(self.mounted_output_dir, self.local_output_dir, 'rw')
        super().run()

    @staticmethod
    def transform_single_file(input_dir,
                              output_dir,
                              input_filename):

        # Docker only accepts absolute path names as argument for its volumes
        # to be mounted:
        absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)
        absolute_path_output_dir = os.path.join(os.getcwd(), output_dir)
        container = DockerXML2RDF()
        container.set_mounted_input_directory(absolute_path_input_dir)
        container.set_mounted_output_directory(absolute_path_output_dir)
        container.set_input_filename(input_filename)
        container.run()

        output_filename = '.'.join( input_filename.split('.')[:-1] + ['ttl'] )
        full_output_filepath = os.path.join(absolute_path_output_dir, output_filename)
        if not os.path.isfile(full_output_filepath):
            logging.error(
                f'Output file {output_filename} not found. Exiting.')
            sys.exit(1)
