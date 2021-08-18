import os
import sys
import logging
import shutil
from docker_split_buildings import DockerSplitBuilding


class DemoSplitBuildings:
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the split buildings algorithm for designating its input/output 
    directories and filenames
    """

    @staticmethod
    def derive_output_file_basename_from_input(input_filename):
        input_filename = os.path.basename(input_filename)
        input_no_extension = input_filename.rsplit('.', 1)[0]
        return input_no_extension + '_splited.gml'

    @staticmethod
    def run_single(vintage,
                   input_directory, input_filename, 
                   output_directory, output_filename):
        if isinstance(vintage, int):
                    vintage = str(vintage)
                    
        if not os.path.isdir(output_directory):
            os.makedirs(output_directory)

        if vintage != '2009' and vintage != '2012' :
            # It happens that 2015 citygml files are already properly split and
            # hence we simply copy them to the output
            shutil.copy(os.path.join(input_directory, input_filename),
                        os.path.join(output_directory,output_filename))
            logging.info(f'DemoSplitBuildings: citygml file {input_filename} was already cleanly split.')
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

