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
        self.input_filename = None
        self.input_ontology = None
        self.input_mappingfile = None

    def assert_ready_for_run(self):
        if len(os.listdir(self.mounted_input_dir)) == 0:
            logging.error('Input directory is empty. Exiting')
            sys.exit(1)
        if self.input_filename is None:
            logging.error('Missing input_filename for running. Exiting')
            sys.exit(1)
        if self.input_ontology is None:
            logging.error('Missing input_ontology for running. Exiting')
            sys.exit(1)
        if self.input_mappingfile is None:
            logging.error('Missing input_mappingfile for running. Exiting')
            sys.exit(1)

    def set_input_filename(self, input_filename):
        full_input_filename = os.path.join(self.mounted_input_dir,
                                           input_filename)
        if not os.path.isfile(full_input_filename):
            logging.error(f'Input file {full_input_filename} not found. Exiting')
            sys.exit(1)
        self.input_filename = input_filename

    def set_input_ontology(self, input_ontology):
        full_input_ontology = os.path.join(self.mounted_input_dir,
                                           input_ontology)
        if not os.path.isdir(full_input_ontology):
            logging.error(f'Input ontology {full_input_ontology} not found. Exiting')
            sys.exit(1)
        self.input_ontology = input_ontology

    def set_input_mappingfile(self, input_mappingfile):
        full_input_mappingfile = os.path.join(self.mounted_input_dir,
                                           input_mappingfile)
        if not os.path.isfile(full_input_mappingfile):
            logging.error(f'Input file {full_input_mappingfile} not found. Exiting')
            sys.exit(1)
        self.input_mappingfile = input_mappingfile

    def get_command(self):
        self.assert_ready_for_run()
        # We don't need to specify the executable since an entrypoint
        # is specified in the DockerFile
        command = (f'xml2rdf {self.input_filename} '
                           f'{self.input_ontology} '
                           f'{self.input_mappingfile}')
        logging.info(f'command: {command}')
        return command

    def run(self):
        # Set input and output volumes
        self.add_volume(self.mounted_input_dir, '/inout/', 'rw')
        super().run()

    @staticmethod
    def transform_single_file(input_dir,
                              input_filename,
                              input_ontology,
                              input_mappingfile):

        # Docker only accepts absolute path names as argument for its volumes
        # to be mounted:
        absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)
        container = DockerXML2RDF()
        container.set_mounted_input_directory(absolute_path_input_dir)
        container.set_input_filename(input_filename)
        container.set_input_ontology(input_ontology)
        container.set_input_mappingfile(input_mappingfile)
        container.run()

        output_filename = '.'.join( input_filename.split('.')[:-1] + ['ttl'] )
        full_output_filepath = os.path.join(absolute_path_input_dir, output_filename)
        if not os.path.isfile(full_output_filepath):
            logging.error(
                f'Output file {full_output_filepath} not found. Exiting.')
            sys.exit(1)
