import logging
import os
import sys
import demo_configuration

# FIXME: is that the inputsOutputs for one file or for multiple files ? Since
#  the strip process treats only one file at a time, it should be for one
#  file ? Currently this class seems to mix those approaches (for one file or
#  for multiple files)
class StripInputsOutputs:
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the strip algorithms for designating its input/output directories
    and filenames
    """
    # FIXME: add several output options (e.g. using an enum) :
    #  next_to_imput_dir,
    def __init__(self,
                 input_dir=demo_configuration.output_dir,
                 output_dir=demo_configuration.output_dir,
                 vintages=demo_configuration.vintages,
                 boroughs=demo_configuration.boroughs):
        self.input_dir = input_dir
        self.output_dir = output_dir
        # FIXME: these two arguments may be directly used from
        #  demo_configuration since we import it ?
        self.vintages = vintages
        self.boroughs = boroughs

    # FIXME: ambiguous name since it does not returns self.output_dir but a
    #  so called "resulting dir". Can we reduce the entropy and avoid having
    #  to much input/output files/folders?
    def get_output_dir(self, vintage, borough, create=True):
        """
        :param vintage: a integer or string designating a year
        :param create: when the proposed output directory does not already
               exist and when create is True then create the output directory
        :return: the proposed output directory of the strip attribute
        """
        if isinstance(vintage, int):
            vintage = str(vintage)
        strip_dir = borough + vintage
        result_dir = os.path.join(self.output_dir, strip_dir)
        if create and not os.path.isdir(result_dir):
            logging.info(f'Creating strip output directory {result_dir}.')
            os.mkdir(result_dir)
        return result_dir

    # FIXME: add the possibility to pass a (list of) vintage and/or a (
    #  list of) borough to allow
    #  to get all filenames or only for a vintage and/or borough
    def get_resulting_files_basenames(self):
        """
        :return: the list of the basename (no directory) filenames that the
                 strip algorithm is supposed to produce
        """
        result = list()
        for vintage in self.vintages:
            for borough in self.boroughs:
                result.append(
                    borough + '_BATI_' + str(vintage) + '_splited_stripped.gml')
        return result

    def get_resulting_filenames(self):
        """
        :return: the list of filenames (includes the directory name relative
                 to the invocation directory) that the strip algorithm is
                 supposed to produce
        """
        result = list()
        for filename in self.get_resulting_files_basenames():
            result.append(os.path.join(self.output_dir, filename))
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

    @staticmethod
    def strip_single_file(container,
                          input_dir,
                          input_filename,
                          output_dir=None,
                          output_filename=None):
        """
        A function to be used to manually handle a single file
        :param container: a DockerStripAttributes instance
        :param input_dir: the directory where the input file is to be found
        :param input_filename: the name of the input file
        :param output_filename: the name of the output file
        :param output_dir: the directory where the output file is to be placed
        :return: the output filename
        """
        if not output_filename:
            output_filename = \
                StripInputsOutputs.derive_output_file_basename_from_input(
                    input_filename)

        # Docker only accepts absolute path names as argument for its volumes
        # to be mounted:
        absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)

        container.set_mounted_input_directory(absolute_path_input_dir)
        container.set_mounted_output_directory(
            container.get_mounted_input_directory())
        container.set_input_filename(input_filename)
        container.set_output_filename(output_filename)
        container.run()

        full_output_filename = os.path.join(input_dir, output_filename)
        logging.info(f'Striping to yield file {full_output_filename}.')
        if not os.path.isfile(full_output_filename):
            logging.error(
                f'Output file {full_output_filename} not found. Exiting.')
            sys.exit(1)

        if not output_dir:
            return full_output_filename
        else:
            # Since CityGML2Stripper does not allow to specify an output folder,
            # we need to "manually" move the resulting file
            target_filename = os.path.join(output_dir, output_filename)
            logging.info(f'Moving resulting file from {full_output_filename} ')
            logging.info(f'to {target_filename}.')
            os.replace(full_output_filename, target_filename)
            return target_filename
