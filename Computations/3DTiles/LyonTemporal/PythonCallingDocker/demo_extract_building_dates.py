import os
import sys
import logging
from docker_extract_building_dates import DockerExtractBuildingDates
from demo import DemoWithFileOutput


class DemoExtractBuildingDates(DemoWithFileOutput):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the extract building dates algorithm for designating its 
    input/output directories and filenames
    """
    def __init__(self):
        super().__init__()

    def get_vintages_result_dir(self, first_vintage, second_vintage, create=True):
        """
        :param first_vintage: a first integer or string designating a year
        :param second_vintage: a second integer or string designating a year
        :param create: when the proposed output directory does not already
               exist and when create is True then create the output directory
        :return: the proposed directory where the results of the extract algorithm
                 will be located. Note that the result directory is a sub-directory
                 of self.output_dir
        """
        if isinstance(first_vintage, int):
            first_vintage = str(first_vintage)
        if isinstance(second_vintage, int):
            second_vintage = str(second_vintage)

        vintages_dir = first_vintage + '_' + second_vintage + '_' + 'Differences'
        vintages_dir = os.path.join(self.get_output_dir(), vintages_dir)
        if create and not os.path.isdir(vintages_dir):
            logging.info(f'Creating extract building dates output directory {vintages_dir}.')
            os.makedirs(vintages_dir)
        return vintages_dir
    
    def get_vintage_borough_output_file_basename(self, vintage, borough):
        raise NotImplementedError()

    def get_borough_vintages_output_file_basename(self, borough, first_vintage, second_vintage):
        # We concatenate the result_dir to the file (base) name for tracability reasons
        # (which allows at later stages to distinguish such files even if the directory
        # layout was changed)
        return borough + '_' + first_vintage + '_' + second_vintage + '-DifferencesAsGraph.json'

    def get_borough_result_dir(self, borough, first_vintage, second_vintage, create=True):
        """
        :param borough: the considered borough
        :param first_vintage: a first integer or string designating a year
        :param second_vintage: a second integer or string designating a year
        :param create: when the proposed output directory does not already
               exist and when create is True then create the output directory
        :return: the proposed directory where the results of the strip attribute
                 will be located. Note that the result directory is a sub-directory
                 of self.output_dir
        """
        if isinstance(first_vintage, int):
            first_vintage = str(first_vintage)
        if isinstance(second_vintage, int):
            second_vintage = str(second_vintage)

        vintages_dir = self.get_vintages_result_dir(first_vintage, second_vintage, create)
        borough_dir = borough + '_' + first_vintage + '_' + second_vintage
        result_dir = os.path.join(vintages_dir, borough_dir)
        if create and not os.path.isdir(result_dir):
            logging.info(f'Creating extract building dates output directory {result_dir}.')
            os.mkdir(result_dir)
        return result_dir

    def get_vintages_resulting_filenames(self, first_vintage, second_vintage, create=True):
        """
        :param first_vintage: a first integer or string designating a year
        :param second_vintage: a second integer or string designating a year
        :param create: when the proposed output directory does not already
               exist and when create is True then create the output directory
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the extract building dates
                 algorithm is supposed to produce for the given vintages
        """
        result = list()
        for borough in self.boroughs:
            result_filename = os.path.join(
                self.get_borough_result_dir(borough, first_vintage, second_vintage, create),
                self.get_borough_vintages_output_file_basename(borough, 
                                                               first_vintage, 
                                                               second_vintage))
            result.append(result_filename)
        return result

    def get_resulting_filenames(self):
        """
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce
        """
        result = list()
        for vintage_index in range(len(self.vintages) - 1):
            first_vintage = str(self.vintages[vintage_index])
            second_vintage = str(self.vintages[vintage_index + 1])
            result.extend(
                self.get_vintages_resulting_filenames(first_vintage, second_vintage, False))
        return result

    def run(self):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("ExtractBuildingDates misses some of its input files: exiting")
            sys.exit(1)
        self.create_output_dir()   # Just making sure

        for vintage_index in range(len(self.vintages) - 1):
            first_vintage = str(self.vintages[vintage_index])
            second_vintage = str(self.vintages[vintage_index + 1])
            # Make sure the output directory exists:
            self.get_vintages_result_dir(first_vintage, second_vintage, create=True)

            for borough in self.boroughs:    
                first_file = input.get_vintage_borough_output_filename(first_vintage,
                                                                       borough)
                second_file = input.get_vintage_borough_output_filename(second_vintage,
                                                                        borough)
                DockerExtractBuildingDates.single_extract(
                    first_vintage,
                    first_file,
                    second_vintage,
                    second_file,
                    self.get_borough_result_dir(borough, first_vintage, second_vintage))
                # We need to rename the default name to demo compatible choices
                source_filename = os.path.join(
                    self.get_borough_result_dir(borough, first_vintage, second_vintage),
                    'DifferencesAsGraph.json')
                target_filename = os.path.join(
                    self.get_borough_result_dir(borough, first_vintage, second_vintage),
                    self.get_borough_vintages_output_file_basename(borough, 
                                                                   first_vintage, 
                                                                   second_vintage))

                os.rename(source_filename, target_filename)
                logging.info(f'ExtractBuildingDates output {source_filename} renamed '
                             f'to {target_filename}.')

