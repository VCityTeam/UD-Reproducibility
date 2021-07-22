import os
import sys
import logging
import jinja2
from docker_helper import DockerHelperPull, DockerHelperTask


class DockerLoad3DCityDB(DockerHelperPull, DockerHelperTask):

    def __init__(self, db_config):
        super().__init__('3dcitydb/impexp', '4.3.0')
        
        # Variables
        self.command = None
        self.files_to_import = list()
        self.importation_dir = None

        # Methods
        self.pull()
        self.__init__comand__line(db_config)


    def __init__comand__line(self, db_config):
        """
        The 3dCityDB-importer requires a configuration with an ad-hoc (xml format) 
        file that must be generated out of the demo_configuration file.  
        """
        
         # Check that db configuration is well defined
        if (('PG_HOST' not in db_config)
                or ('PG_USER' not in db_config)
                or ('PG_PORT' not in db_config)
                or ('PG_NAME' not in db_config)
                or ('PG_USER' not in db_config)
                or ('PG_PASSWORD' not in db_config)):
            logging.error('Database is not properly defined in ' +
                          self.config_file + ', please refer to README.md')
            sys.exit(1)

        self.command = 'import '
        self.command += '-H ' + db_config['PG_HOST'] + ' '
        self.command += '-d ' + db_config['PG_NAME'] + ' '
        self.command += '-u ' + db_config['PG_USER'] + ' '
        self.command += '-p ' + db_config['PG_PASSWORD'] + ' '
        self.command += '-P ' + db_config['PG_PORT']

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
        if not self.command:
            logging.error('Importer/exporter : Importer command line is NULL ')
            sys.exit(1)
        for file in self.files_to_import:
            self.command += ' /InputFiles/' + file + ' '
        logging.info('Command launch : ' + self.command)
        return self.command

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
