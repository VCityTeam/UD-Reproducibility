import logging
import os
import sys
import demo_configuration
import docker_strip_attributes


class DemoStrip:
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the strip algorithms for designating its input/output directories
    and filenames
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

    def get_result_dir(self, vintage, create=True):
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
        result_dir = os.path.join(self.output_dir, strip_dir)
        if create and not os.path.isdir(result_dir):
            logging.info(f'Creating strip output directory {result_dir}.')
            os.mkdir(result_dir)
        return result_dir

    def get_vintage_borough_resulting_filename(self, vintage, borough):
        """
        :return: the filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce for the given vintage and borough
        """
        return os.path.join(
                self.get_result_dir(vintage, False),
                borough + '_BATI_' + str(vintage) + '_splited_stripped.gml')

    def get_vintage_resulting_filenames(self, vintage):
        """
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce for given vintage
        """
        result = list()
        for borough in self.boroughs:
            result.append(self.get_vintage_borough_resulting_filename(vintage, 
                                                                      borough))
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

    @staticmethod
    def derive_output_file_basename_from_input(input_filename):
        input_filename = os.path.basename(input_filename)
        input_no_extension = input_filename.rsplit('.', 1)[0]
        return input_no_extension + '_stripped.gml'

    def run(self):
        for vintage in self.vintages:
            vintage_inputs = list()
            for borough in self.boroughs:
                # FIXME: the name of the output of the split algorithm should
                # NOT be hardwired here but obtained out of DemoSplit
                input_filename = os.path.join(
                     self.output_dir,
                     borough + '_' + str(vintage),
                     borough + '_BATI_' + str(vintage) + '_splited.gml')

                docker_strip_attributes.strip_single_file(
                    docker_strip_attributes.DockerStripAttributes(),
                    input_dir=os.path.dirname(input_filename),
                    input_filename=os.path.basename(input_filename),
                    output_filename=DemoStrip.derive_output_file_basename_from_input(input_filename),
                    output_dir=self.get_result_dir(vintage))

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    strip = DemoStrip()
    strip.run()
    strip.assert_output_files_exist()
    print("Resulting stripped files", strip.get_resulting_filenames())
