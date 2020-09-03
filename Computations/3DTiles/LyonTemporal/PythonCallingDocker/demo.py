import os
import sys
import logging
import demo_configuration


class Demo:
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the various derived demonstration classes in order to designate
    their respective input/output directories and filenames
    """
    def __init__(self,
                 input_dir=demo_configuration.output_dir,
                 output_dir=demo_configuration.output_dir,
                 city=demo_configuration.city,
                 vintages=demo_configuration.vintages,
                 boroughs=demo_configuration.boroughs):
        self.city = city
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.vintages = vintages
        self.boroughs = boroughs

    def __init_databases__(self):
        if not demo_configuration.databases:
            logging.info(f'Databases configurations not found. Exiting')
            sys.exit(1)
        
        self.databases = demo_configuration.databases
        
        for vintage in self.vintages:
            if not self.databases[vintage]:
                logging.info(f'Database configuration for vintage {vintage} was not '
                            f'found. You must specify one database configuration '
                            f'per vintage. Exiting')
                sys.exit(1)

    def get_vintage_borough_initial_directory(self, vintage, borough):
        """
        :return: the directory name for the given vintage and borough
                 as layed out after the download and patch.
        FIXME: this method should be in the lyon_metropole_download_and_patch
        demo class.
        """
        return os.path.join(self.output_dir, borough + '_' + str(vintage))

    @staticmethod
    def get_vintage_borough_filename(vintage, borough):
        """
        :return: the filename for the given vintage and borough
                 as layed out after the download and patch. This function
                 does NOT include the directory (relative to self.output_dir)
                 in which it lies.
        FIXME: this method should be in the lyon_metropole_download_and_patch
        demo class.
        """
        return borough + '_BATI_' + str(vintage) + '.gml'

    def get_resulting_filenames(self):
        raise NotImplementedError()

    def assert_output_files_exist(self):
        """
        :return: True when all the strip produced files exist in the default
                 place (i.e. when an alternate output_dir was not specified)
                 False otherwise.
        """
        for filename in self.get_resulting_filenames():
            if not os.path.isfile(filename):
                logging.error(f'Output file {filename} not found.')
                return False
        return True
