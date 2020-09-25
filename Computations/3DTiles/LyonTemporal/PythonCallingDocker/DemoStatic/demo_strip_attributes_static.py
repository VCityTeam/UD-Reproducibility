import logging
import os
import sys

from demo_static import DemoWithFileOutputStatic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from demo_strip_attributes import DemoStrip
from docker_strip_attributes import DockerStripAttributes


class DemoStripStatic(DemoStrip, DemoWithFileOutputStatic):

    def __init__(self):
        super().__init__()

    def get_result_dir(self, create=True):
        """
        :param create: when the proposed output directory does not already
               exist and when create is True then create the output directory
        :return: the proposed directory where the results of the strip attribute
                 will be located. Note that the result directory is a sub-directory
                 of self.output_dir
        """
        strip_dir = self.city + '_' + str(self.vintage) + '_Stripped'
        result_dir = os.path.join(self.get_output_dir(), strip_dir)
        if create and not os.path.isdir(result_dir):
            logging.info(f'Creating strip output directory {result_dir}.')
            os.mkdir(result_dir)
        return result_dir

    def get_borough_output_directory_name(self, borough):
        # Borough names get flatened out and simply disregarded
        return self.get_result_dir(False)

    def get_borough_output_file_basename(self, borough):
        """
        :return: the filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce for the given vintage and borough
        """
        input_filename = self.input_demo.get_borough_output_filename(borough)
        return DemoStrip.derive_output_file_basename_from_input(input_filename)

    def get_resulting_filenames(self):
        """
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce for given vintage
        """
        result = list()
        for borough in self.boroughs:
            result.append(self.get_borough_output_filename(borough))
        return result

    def run(self):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("Strip misses some of its input files: exiting")
            sys.exit(1)
        self.create_output_dir()   # Just making sure

        for borough in self.boroughs:
            DockerStripAttributes.strip_single_file(
                input_dir = input.get_borough_output_directory_name(borough),
                input_filename = input.get_borough_output_file_basename(borough),
                output_filename = self.get_borough_output_file_basename(borough),
                output_dir=self.get_result_dir())
