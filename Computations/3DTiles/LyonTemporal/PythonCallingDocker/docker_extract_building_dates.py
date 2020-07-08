import os
import sys
import logging
from docker_3duse import Docker3DUse
import demo_configuration as demo


class DockerExtractBuildingDates(Docker3DUse):

    def __init__(self):
        super().__init__()
        self.working_dir = '/root/3DUSE/Build/src/utils/cmdline/'
        self.first_date = None
        self.second_date = None
        self.first_input_filename = None
        self.second_input_filename = None
        self.command_output_directory = None

    def assert_ready_for_run(self):
        if not self.first_date:
            logging.info('Missing first_date for running. Exiting')
            sys.exit(1)
        if not self.second_date:
            logging.info('Missing second_date for running. Exiting')
            sys.exit(1)
        if not self.first_input_filename:
            logging.info('Missing first_input_filename for running. Exiting')
            sys.exit(1)
        if not self.second_input_filename:
            logging.info('Missing second_input_filename for running. Exiting')
            sys.exit(1)

    def set_first_date(self, date):
        self.first_date = date

    def set_second_date(self, date):
        self.second_date = date

    def set_first_input_filename(self, first_input_filename):
        full_first_input_filename = os.path.join(self.mounted_input_dir,
                                                 first_input_filename)
        if not os.path.isfile(full_first_input_filename):
            logging.info(f'Input file {full_first_input_filename} not found.'
                         ' Exiting')
            sys.exit(1)
        self.first_input_filename = first_input_filename

    def set_second_input_filename(self, second_input_filename):
        full_second_input_filename = os.path.join(self.mounted_input_dir,
                                                  second_input_filename)
        if not os.path.isfile(full_second_input_filename):
            logging.info(f'Input file {full_second_input_filename} not found.'
                         ' Exiting')
            sys.exit(1)
        self.second_input_filename = second_input_filename

    def set_command_output_directory(self, output_directory):
        # This is internal to the container and as seen by the container
        # command (as opposed to the directory mounted from "outside" the
        # container i.e. DockerHelper.mounted_output_dir)
        self.command_output_directory = output_directory

    def get_command(self):
        self.assert_ready_for_run()
        command = 'extractBuildingDates '   # Mind the trailing separator

        command += '--first_date ' + self.first_date + ' '
        command += '--first_file /Input/' + self.first_input_filename + ' '

        command += '--second_date ' + self.second_date + ' '
        command += '--second_file /Input/' + self.second_input_filename + ' '

        if self.mounted_input_dir == self.mounted_output_dir:
            # Because mounting twice the same directory will be avoided
            # in the DockerHelp.run() method.
            command += '--output_dir /Input/'
        else:
            command += '--output_dir /Output/'
        if self.command_output_directory:
            command += self.command_output_directory + ' '
        return command


def single_extract(input_dir,
                   first_date,
                   first_input_filename,
                   second_date,
                   second_input_filename,
                   output_dir):
    d = DockerExtractBuildingDates()
    # Docker only accepts absolute path names as argument for its volumes
    # to be mounted:
    absolute_path_input_dir = os.path.join(os.getcwd(), input_dir)
    d.set_mounted_input_directory(absolute_path_input_dir)
    absolute_path_output_dir = os.path.join(os.getcwd(), output_dir)
    d.set_mounted_output_directory(absolute_path_output_dir)

    d.set_first_date(first_date)
    d.set_first_input_filename(first_input_filename)
    d.set_second_date(second_date)
    d.set_second_input_filename(second_input_filename)

    d.run()

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='docker_split_buildings.log',
                        filemode='w')

    # Note: there is probably something simpler to be done with
    # LyonMetropoleDowloadAndSanitize.get_resulting_filenanes() but we
    # cannot access it in this context
    inputs = list()
    for borough in demo.boroughs:
        for vintage_index in range(len(demo.vintages)-1):
            first_date = str(demo.vintages[vintage_index])


            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA


            first_file = os.path.join(demo.output_dir,
                                      borough + '_' + first_date,
                                      borough + '_BATI_' + first_date + '.gml')
            second_date = str(demo.vintages[vintage_index+1])
            inputs.append(
                [v_first,
                 os.path.join(demo.output_dir, borough + '_' + str(vintage)),


                 borough + '_BATI_' + str(vintage) + '.gml',
                 borough + '_BATI_' + str(vintage) + '_splited.gml'])

    for f in files[0:0]:
        print("Now handling", f)
        split(first_date=f[0],
              first_input_filename=f[1],
              second_date=f[2],
              second_input_filename=f[3],
              )

