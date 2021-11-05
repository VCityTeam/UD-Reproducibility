import os
import sys
import logging
from abc import ABC, abstractmethod


class Demo:
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the various derived demonstration classes in order to designate
    their respective input/output directories and filenames
    """
    def __init__(self,
                 results_dir = None,
                 all_demos_output_dir = None,
                 city = None,
                 boroughs = None):

        # The all_demos_output_dir directory is the directory within which all the 
        # demos (i.e. demonstatrion classes inheriting from this Demo class) will 
        # place their outputs. Note that the actual outputs of a particular demo
        # can be in a sub-directory of all_demos_output_dir (refer to Demo.get_output_dir() 
        # method)
        # FIXME: this should be a class variable
        self.all_demos_output_dir = all_demos_output_dir
        # When self.results_dir is set this Demo will outputs/results will be located in 
        # the "results_dir" sub-directory of self.all_demos_output_dir (refer to 
        # Demo.get_ouput_dir() method).
        self.set_results_dir(results_dir)
        self.city = city
        self.boroughs = boroughs
        self.input_demo = None

    def create_output_dir(self):
        output_dir = self.get_output_dir()
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

    def get_output_dir(self):
        output_dir = self.all_demos_output_dir
        if self.results_dir:
            output_dir = os.path.join(self.all_demos_output_dir, self.results_dir)
        return output_dir

    def set_results_dir(self, results_dir):
        self.results_dir = results_dir

        
class DemoWithFileOutput(ABC):
    """
    Additionnal conventions for demos yielding outputs in the form of files
    (as opposed to e.g. databases) 
    """
    @abstractmethod
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
