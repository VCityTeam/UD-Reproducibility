import os
import sys
import logging
import shutil

from demo_temporal import DemoWithFileOutputTemporal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from docker_split_buildings import DockerSplitBuilding


class DemoSplitBuildings(DemoWithFileOutputTemporal):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the split buildings algorithm for designating its input/output 
    directories and filenames
    """
    def __init__(self):
        super().__init__()

    @staticmethod
    def derive_output_file_basename_from_input(input_filename):
        input_filename = os.path.basename(input_filename)
        input_no_extension = input_filename.rsplit('.', 1)[0]
        return input_no_extension + '_splited.gml'

    def get_vintage_borough_output_file_basename(self, vintage, borough):
        input_filename = self.input_demo.get_vintage_borough_output_filename(vintage, borough)
        return DemoSplitBuildings.derive_output_file_basename_from_input(input_filename)

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
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("Split misses some of its input files: exiting")
            sys.exit(1)
        self.create_output_dir()   # Just making sure

        for borough in self.boroughs:
            for vintage in self.vintages:
                if isinstance(vintage, int):
                    vintage = str(vintage)
                input_directory = input.get_vintage_borough_output_directory_name(vintage, borough)
                input_filename = input.get_vintage_borough_output_file_basename(vintage, borough)
                output_directory = self.get_vintage_borough_output_directory_name(vintage,borough)
                output_filename = self.get_vintage_borough_output_file_basename(vintage, borough)

                if not os.path.isdir(output_directory):
                    os.mkdir(output_directory)

                if vintage == '2015':
                    # It happens that 2015 citygml files are already properly split and
                    # hence we simply copy them to the output
                    shutil.copy(os.path.join(input_directory, input_filename),
                                os.path.join(output_directory,output_filename))
                else:
                    # For other vintages (2009, 2012) we need to get the job done:
                    DockerSplitBuilding.split(
                        input_directory,
                        input_filename,
                        output_filename)
                    logging.info(f'DemoSplitBuildings: citygml file {input_filename} was split.')
                    # Because the split method doesn't know how to specify an output directory
                    # (it this so hard?) by default it places its result side by side with the
                    # input file. We thus need to move the resulting file
                    shutil.move(os.path.join(input_directory, output_filename),
                                os.path.join(output_directory,output_filename))

