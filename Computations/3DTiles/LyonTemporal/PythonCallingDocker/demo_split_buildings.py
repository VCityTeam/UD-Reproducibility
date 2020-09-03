import os
import sys
import logging
from docker_split_buildings import DockerSplitBuilding
from demo import Demo


class DemoSplitBuildings(Demo):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the split buildings algorithm for designating its input/output 
    directories and filenames
    """
    def __init__(self):
        Demo.__init__(self)

    @staticmethod
    def derive_output_file_basename_from_input(input_filename):
        input_filename = os.path.basename(input_filename)
        input_no_extension = input_filename.rsplit('.', 1)[0]
        return input_no_extension + '_splited.gml'

    def get_vintage_borough_input_file_basename(self, vintage, borough):
        return Demo.get_vintage_borough_filename(vintage, borough)

    def get_vintage_borough_output_file_basename(self, vintage, borough):
        input_filename = self.get_vintage_borough_input_file_basename(vintage, borough)
        output_filename = DemoSplitBuildings.derive_output_file_basename_from_input(
                    input_filename)
        return output_filename

    def get_vintage_borough_output_filename(self, vintage, borough):
        input_directory = self.get_vintage_borough_initial_directory(vintage, borough)
        input_filename = self.get_vintage_borough_input_file_basename(vintage, borough)
        output_directory = input_directory
        output_filename = self.get_vintage_borough_output_file_basename(vintage, borough)
        return os.path.join(output_directory, output_filename)

    def get_resulting_filenames(self):
        """
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the split algorithm is
                 supposed to produce
        """
        result = list()
        for borough in self.boroughs:
            for vintage in self.vintages:
                result.append(self.get_vintage_borough_output_filename(vintage, borough))
        return result

    def run(self):
        for borough in self.boroughs:
            for vintage in self.vintages:
                input_directory = self.get_vintage_borough_initial_directory(vintage, borough)
                input_filename = self.get_vintage_borough_input_file_basename(vintage, borough)
                output_filename = self.get_vintage_borough_output_file_basename(vintage, borough)
                logging.info(f'DemoSplitBuildings: spliting citygml file {input_filename}.')
                DockerSplitBuilding.split(
                    input_directory,
                    input_filename,
                    output_filename)

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    split = DemoSplitBuildings()
    split.run()
    split.assert_output_files_exist()
    print("Resulting stripped files", split.get_resulting_filenames())