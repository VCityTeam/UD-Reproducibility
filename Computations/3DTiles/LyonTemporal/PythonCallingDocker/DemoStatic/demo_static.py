import os
import sys
import logging
from abc import ABC, abstractmethod

import demo_configuration_static

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from demo import Demo, DemoWithFileOutput



class DemoStatic(Demo):
    def __init__(self,
                results_dir = None,
                all_demos_output_dir = demo_configuration_static.output_dir,
                city=demo_configuration_static.city,
                boroughs=demo_configuration_static.boroughs):
        super().__init__(results_dir, all_demos_output_dir, city, boroughs)


class DemoWithFileOutputStatic(DemoStatic, DemoWithFileOutput, ABC):
    """
    Additionnal conventions structuring the file layout 
    """
    @abstractmethod
    def get_borough_output_file_basename(self, borough):
        raise NotImplementedError()

    def get_borough_output_directory_name(self, borough):
        return os.path.join(self.get_output_dir(), borough)

    def get_borough_output_filename(self, borough):
        """
        :return: the filename for the given borough as layed out after the 
                 download and patch. This function result DOES include the directory 
                 name in which the output file lies.
        """
        return os.path.join(self.get_borough_output_directory_name(borough),
                            self.get_borough_output_file_basename(borough))


class DemoWithDataBaseStatic:

    def __init_database__(self):
        if not demo_configuration_static.database:
            logging.info(f'Database configuration not found. Exiting')
            sys.exit(1)

        self.database = demo_configuration_static.database
