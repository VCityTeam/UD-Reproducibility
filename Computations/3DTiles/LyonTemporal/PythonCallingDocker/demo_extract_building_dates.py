import os
import sys
import logging
import demo_configuration
from demo_strip_attributes import DemoStrip
from docker_extract_building_dates import DockerExtractBuildingDates


class DemoExtractBuildingDates:
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the extract building dates algorithm for designating its 
    input/output directories and filenames
    """
    def __init__(self,
                 input_dir=demo_configuration.output_dir,
                 output_dir=demo_configuration.output_dir,
                 city=demo_configuration.city,
                 vintages=demo_configuration.vintages,
                 boroughs=demo_configuration.boroughs):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.city = city
        self.vintages = vintages
        self.boroughs = boroughs

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
        vintages_dir = os.path.join(self.output_dir, vintages_dir)
        if create and not os.path.isdir(vintages_dir):
            logging.info(f'Creating extract building dates output directory'
                          '{vintages_dir}.')
            os.mkdir(vintages_dir)
        return vintages_dir

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
        borough_dir = borough + '_' + first_vintage + '-' + second_vintage
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
                'DifferencesAsGraph.json')
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

    def assert_output_files_exist(self):
        """
        :return: True when all the strip produced files exist in the default
                 place (i.e. when an alternate output_dir was not specified)
                 False otherwise.
        """
        for filename in self.get_resulting_filenames():
            if not os.path.isfile(filename):
                logging.error(f'Strip output file {filename} not found.')
                return False
        return True

    def run(self):
        strip = DemoStrip()
        for vintage_index in range(len(self.vintages) - 1):
            first_vintage = str(self.vintages[vintage_index])
            second_vintage = str(self.vintages[vintage_index + 1])
            for borough in self.boroughs:

                # Make sure the output directory exists:
                output_dir = self.get_vintages_result_dir(first_vintage,
                                                          second_vintage,
                                                          create=True)

                first_file = strip.get_vintage_borough_resulting_filename(first_vintage,
                                                                          borough)
                second_file = strip.get_vintage_borough_resulting_filename(second_vintage,
                                                                          borough)
                DockerExtractBuildingDates.single_extract(
                    first_vintage,
                    first_file,
                    second_vintage,
                    second_file,
                    self.get_borough_result_dir(borough, first_vintage, second_vintage))


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    extract = DemoExtractBuildingDates()
    extract.run()
    extract.assert_output_files_exist()
    print("Resulting extracted building dates files", 
          extract.get_resulting_filenames())
