import os
import sys
import logging
from docker_helper import DockerHelperBuild, DockerHelperTask


class DockerLoad3DCityDB(DockerHelperBuild, DockerHelperTask):

    def __init__(self):
        super().__init__('tumgis/3dcitydb-impexp', '4.2.3')

        # Note: old method with git clone, now we build the docker from a local
        # DockerFile (see ../Docker/3DCityDB-ImpExp-DockerContext/Readme.md)
        # extraction_dir = os.path.join(
        #     os.getcwd(),
        #     '3dcitydb-importer-exporter-docker.git')
        # if os.path.isdir(extraction_dir):
        #     logging.info(f'Extraction directory {extraction_dir} already '
        #                  'exists. Using the existing one (that might not '
        #                  'be up to date or on the proper branch...')
        # else:
        #     repository = \
        #         "https://github.com/tum-gis/3dcitydb-importer-exporter-docker"
        #     git.Repo.clone_from(repository, extraction_dir)

        this_file_dir = os.path.dirname(os.path.realpath(__file__))
        context_dir = os.path.join(this_file_dir,
                                   '..',
                                   'Docker',
                                   '3DCityDBImpExp-DockerContext')
        self.build(context_dir)

        self.configuration_filename = None
        self.configuration_dir = None
        self.files_to_import = list()
        self.importation_dir = None

    def assert_ready_for_run(self):
        if not self.configuration_filename:
            logging.info('Missing configuration_filename for running. Exiting')
            sys.exit(1)
        if not self.importation_dir:
            logging.info('Missing importation_dir for running. Exiting')
            sys.exit(1)

    def set_configuration_filename(self, configuration_filename):
        """
        :param input_filename: absolute filename of the configuration file
        """
        # Assert this is indeed an absolute pathname
        if not os.path.isfile(configuration_filename):
            logging.info(f'Configuration file {configuration_filename} '
                         f'not found. Exiting')
            sys.exit(1)
        if not os.path.isabs(configuration_filename):
            logging.info(f'Configuration filename {configuration_filename} '
                         f'is not absolute. Exiting')
            sys.exit(1)
        self.configuration_filename = os.path.basename(configuration_filename)
        self.configuration_dir = os.path.dirname(configuration_filename)
        self.add_volume(self.configuration_dir, '/InputConfig', 'rw')

    def set_files_to_import(self, files):
        if not type(files) is list:
            logging.info(f'Files argument must be a list but got {files} '
                         f'Exiting')
            sys.exit(1)
        for file in files:
            if not os.path.isfile(file):
                logging.info(f'File to import {file} not found. Exiting')
                sys.exit(1)
            if not os.path.isabs(file):
                logging.info(f'File to import {file} is not absolute. Exiting')
                sys.exit(1)
            if not self.importation_dir:
                self.importation_dir = os.path.dirname(file)
            else:
                if not self.importation_dir == os.path.dirname(file):
                    logging.error(f'Files to import must belong to same '
                                  f'directory but got:')
                    logging.error(f'   {files}')
                    logging.error(f'Exiting.')
                    sys.exit(1)
            self.files_to_import.append(os.path.basename(file))
        self.add_volume(self.importation_dir, '/InputFiles', 'rw')

    def get_command(self):
        self.assert_ready_for_run()
        command = '-config '  # Mind the trailing separator
        command += '/InputConfig/' + self.configuration_filename + ' '

        command += '-import '
        for file in self.files_to_import:
            command += '/InputFiles/' + file + ';'

        return command
