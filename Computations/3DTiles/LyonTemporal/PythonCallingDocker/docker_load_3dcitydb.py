import os
import sys
import logging
import git
from docker_helper import DockerHelperBuild, DockerHelperTask
from docker_3dcitydb_server import Docker3DCityDBServer
import demo_strip_attributes
import demo_configuration as demo


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

        context_dir = os.path.join(os.getcwd(),
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


def import_files(config_file, input_filenames):
    d = DockerLoad3DCityDB()
    d.set_configuration_filename(config_file)
    d.set_files_to_import(input_filenames)
    d.run()


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Note: there is probably something simpler to be done with
    # LyonMetropoleDowloadAndSanitize.get_resulting_filenanes() but we
    # cannot access it in this context

    logging.info('Stage 1: starting databases.')

    active_databases = list()
    for vintage in demo.vintages:
        data_base = Docker3DCityDBServer()
        data_base.set_config_file('DBConfig' + str(vintage) + '.yml')
        data_base.load_config_file()
        data_base.run()
        active_databases.append(data_base)
    logging.info('Stage 1: done.')

    logging.info(f'Stage 2: importing files to databases.')
    for vintage in demo.vintages:
        inputs = list()
        # FIXME: the usage of StripInputsOutputs has been removed from now
        #  until the fixmes of this class are resolved
        for borough in demo.boroughs:
            relative_output_dir = borough + '_' + str(vintage)
            filename = borough + '_BATI_' + str(vintage) + \
                '_splited_stripped.gml'
            filepath = os.path.join(demo.output_dir, relative_output_dir,
                                    filename)
            inputs.append(os.path.abspath(filepath))

        configuration_file = '3dCityDBImpExpConfig-' + str(vintage) + '.xml'
        logging.info(f'Importation for vintage {str(vintage)}: starting.')
        logging.info(f'Files set for importation: {inputs}')
        import_files(os.path.abspath(configuration_file), inputs)
        logging.info(f'Importation for vintage {str(vintage)}: done.')
    logging.info('Stage 2: done')

    logging.info('Stage 3: halting containers.')
    for server in active_databases:
        logging.info(f'   Halting container {server.get_container().name}.')
        server.halt_service()
    logging.info('Stage 3: done')