import logging
import os
import sys

from demo_temporal import DemoWithFileOutputTemporal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from docker_strip_attributes import DockerStripAttributes



class DemoStrip(DemoWithFileOutputTemporal):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the strip algorithms for designating its input/output directories
    and filenames
    """
    def __init__(self):
        super().__init__()
    
    @staticmethod
    def derive_output_file_basename_from_input(input_filename):
        input_filename = os.path.basename(input_filename)
        input_no_extension = input_filename.rsplit('.', 1)[0]
        return input_no_extension + '_stripped.gml'

    def get_vintage_result_dir(self, vintage, create=True):
        """
        :param vintage: a integer or string designating a year
        :param create: when the proposed output directory does not already
               exist and when create is True then create the output directory
        :return: the proposed directory where the results of the strip attribute
                 will be located. Note that the result directory is a sub-directory
                 of self.output_dir
        """
        if isinstance(vintage, int):
            vintage = str(vintage)
        strip_dir = self.city + '_' + vintage + '_Stripped'
        result_dir = os.path.join(self.get_output_dir(), strip_dir)
        if create and not os.path.isdir(result_dir):
            logging.info(f'Creating strip output directory {result_dir} '
                         f'for {vintage} vintage.')
            os.mkdir(result_dir)
        return result_dir

    def get_vintage_borough_output_directory_name(self, vintage, borough):
        # Borough names get flatened out and simply disregarded
        return self.get_vintage_result_dir(vintage)

    def get_vintage_borough_output_file_basename(self, vintage, borough):
        """
        :return: the filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce for the given vintage and borough
        """
        input_filename = self.input_demo.get_vintage_borough_output_filename(vintage, borough)
        return DemoStrip.derive_output_file_basename_from_input(input_filename)

    def get_vintage_resulting_filenames(self, vintage):
        """
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce for given vintage
        """
        result = list()
        for borough in self.boroughs:
            result.append(self.get_vintage_borough_output_filename(vintage, borough))
        return result

    def get_resulting_filenames(self):
        """
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce
        """
        result = list()
        for vintage in self.vintages:
            result.extend(self.get_vintage_resulting_filenames(vintage))
        return result

    def run(self):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("Strip misses some of its input files: exiting")
            sys.exit(1)
        self.create_output_dir()   # Just making sure

        for vintage in self.vintages:
            for borough in self.boroughs:
                DockerStripAttributes.strip_single_file(
                    input_dir = \
                        input.get_vintage_borough_output_directory_name(vintage, borough),
                    input_filename = \
                        input.get_vintage_borough_output_file_basename(vintage, borough),
                    output_filename = \
                        self.get_vintage_borough_output_file_basename(vintage,borough),
                    output_dir=self.get_vintage_result_dir(vintage))
