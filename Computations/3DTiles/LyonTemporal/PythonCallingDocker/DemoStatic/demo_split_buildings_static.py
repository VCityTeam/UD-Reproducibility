import os
import sys
import logging
import shutil
from demo_static import DemoWithFileOutputStatic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from demo_split_buildings import DemoSplitBuildings


class DemoSplitBuildingsStatic(DemoSplitBuildings,
                               DemoWithFileOutputStatic):
    def __init__(self):
        super().__init__()

    def get_borough_output_file_basename(self, borough):
        input_filename = self.input_demo.get_borough_output_filename(borough)
        return DemoSplitBuildings.derive_output_file_basename_from_input(input_filename)

    def get_resulting_filenames(self):
        """
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the split algorithm is
                 supposed to produce
        """
        result = list()
        for borough in self.boroughs:
            result.append(self.get_borough_output_filename(borough))
        return result

    def run(self):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("Split misses some of its input files: exiting")
            sys.exit(1)

        for borough in self.boroughs:
            input_directory = input.get_borough_output_directory_name(borough)
            input_filename = input.get_borough_output_file_basename(borough)
            output_directory = self.get_borough_output_directory_name(borough)
            output_filename = self.get_borough_output_file_basename(borough)
            DemoSplitBuildings.run_single(self.vintage,
                                          input_directory, input_filename, 
                                          output_directory, output_filename)
