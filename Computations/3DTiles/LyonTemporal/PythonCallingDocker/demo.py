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
