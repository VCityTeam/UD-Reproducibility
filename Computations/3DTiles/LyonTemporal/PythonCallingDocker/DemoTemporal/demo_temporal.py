import os
import sys
import logging
from abc import ABC, abstractmethod

import demo_configuration_temporal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from demo import Demo, DemoWithFileOutput


class DemoTemporal(Demo):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the various derived demonstration classes in order to designate
    their respective input/output directories and filenames
    """
    def __init__(self,
                 results_dir = None,
                 all_demos_output_dir =demo_configuration_temporal.output_dir,
                 city=demo_configuration_temporal.city,
                 vintages=demo_configuration_temporal.vintages,
                 boroughs=demo_configuration_temporal.boroughs):

        super().__init__(results_dir, all_demos_output_dir, city, boroughs)
        self.vintages = vintages

class DemoWithFileOutputTemporal(DemoTemporal, DemoWithFileOutput, ABC):
    """
    Additionnal conventions for demos yielding outputs in the form of files
    (as opposed to e.g. databases) 
    """
    @abstractmethod
    def get_vintage_borough_output_file_basename(self, vintage, borough):
        raise NotImplementedError()

    def get_vintage_borough_output_directory_name(self, vintage, borough):
        return os.path.join(self.get_output_dir(), borough + '_' + str(vintage))

    def get_vintage_borough_output_filename(self, vintage, borough):
        """
        :return: the filename for the given vintage and borough as layed out after the 
                 download and patch. This function result DOES include the directory 
                 name in which the output file lies.
        """
        return os.path.join(self.get_vintage_borough_output_directory_name(vintage, borough),
                            self.get_vintage_borough_output_file_basename(vintage, borough))


class DemoWithDataBasesTemporal(DemoTemporal):

    def __init_databases__(self):
        if not demo_configuration_temporal.databases:
            logging.info(f'Databases configurations not found. Exiting')
            sys.exit(1)
        
        self.databases = demo_configuration_temporal.databases
        
        for vintage in self.vintages:
            if not self.databases[vintage]:
                logging.info(f'Database configuration for vintage {vintage} was not '
                            f'found. You must specify one database configuration '
                            f'per vintage. Exiting')
                sys.exit(1)
