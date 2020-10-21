import os
import sys
import logging
import jinja2
from docker_helper import DockerHelperBuild, DockerHelperTask


class DockerLoad3DCityDB(DockerHelperBuild, DockerHelperTask):

    def __init__(self, db_config):
        super().__init__('tumgis/3dcitydb-impexp', '4.2.3')

        context_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                   '..',
                                   'Docker',
                                   '3DCityDBImpExp-DockerContext')
        self.build(context_dir)

        self.configuration_filename = None
        self.configuration_dir = None
        self.__init__configuration_file(db_config)

        self.files_to_import = list()
        self.importation_dir = None

    def __init__configuration_file(self, db_config):
        """
        The 3dCityDB-importer requires a configuration with an ad-hoc (xml format) 
        file that must be generated out of the demo_configuration file.  
        """
        # ### First generate the ad-hoc (xml format) configuration file expected by the 
        # container
        this_file_dir = os.path.dirname(os.path.realpath(__file__))
        # j2_template_file = os.path.join(this_file_dir, '3dCityDBImpExpConfig.j2')
        j2_template_file = '3dCityDBImpExpConfig.j2'

        if not os.path.isfile(os.path.join(this_file_dir, j2_template_file)):
            logging.info(f'Jinja2 template file {j2_template_file} not found. Exiting')
            sys.exit(1)

        # Load template from file system
        template_loader = jinja2.FileSystemLoader(searchpath=[this_file_dir])
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(j2_template_file)

        # Create a TemplateStream object (that can be dumped into a file
        # afterwards) and replace the variables with the values from db_config
        template_stream = template.stream(PG_HOST=db_config['PG_HOST'],
                                          PG_PORT=db_config['PG_PORT'],
                                          PG_NAME=db_config['PG_NAME'],
                                          PG_USER=db_config['PG_USER'],
                                          PG_PASSWORD=db_config['PG_PASSWORD'])
        # We need to refert to the configuration file through its absolute pathname
        # so that we can mount the directory to the container
        configuration_filename = os.path.abspath(
            '3dCityDBImpExpConfig-' + db_config['PG_NAME'] + '.xml')
        template_stream.dump(configuration_filename)

        # Assert the file was properly generated: 
        if not os.path.isfile(configuration_filename):
            logging.info(f'Configuration file {configuration_filename} '
                         f'not found. Exiting')
            sys.exit(1)
        # Just being paranoid: assert this is indeed an absolute pathname
        if not os.path.isabs(configuration_filename):
            logging.info(f'Configuration filename {configuration_filename} '
                         f'is not absolute. Exiting')
            sys.exit(1)

        # ### Preparere the information for the container to mount the directory
        # holding the configuration file and know about its configuratin filename
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
        command = '-config '  # Mind the trailing separator
        command += '/InputConfig/' + self.configuration_filename + ' '

        command += '-import '
        for file in self.files_to_import:
            command += '/InputFiles/' + file + ';'

        return command

    def check_log_result(self, log_filename):
        """
        Assuming that the log_filename files contains the logs of an importation
        round of this class (the run() method was called), check the logs 
        content in order to check whether the files were properly imported.
        """
        if not self.files_to_import:
            logging.error('No files were set up for importation. Exiting.')
            sys.exit(1)
        last_imported_filename = self.files_to_import[-1]
        with open(log_filename, 'r') as f:
            for line in f.readlines():
                if 'Database import successfully finished' in line:
                    if last_imported_filename in line:
                        logging.info(f'{last_imported_filename} file duly imported.')
                        return True
        logging.info('Importation process failed. Exiting.')
        sys.exit(1)
