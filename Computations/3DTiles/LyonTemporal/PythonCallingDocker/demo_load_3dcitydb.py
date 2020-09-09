import os
import sys
import logging
import jinja2
import time

from docker_load_3dcitydb import DockerLoad3DCityDB
from demo_3dcitydb_server import Demo3dCityDBServer
from demo import Demo
import demo_full_workflow as workflow


class DemoLoad3DCityDB(Demo):
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the DockerLoad3DCityDB algorithms for designating its input
    directories and filenames
    """
    
    @staticmethod
    def __get_vintage_configuration_filename(vintage):
        return '3dCityDBImpExpConfig' + str(vintage) + '.xml'

    @staticmethod
    def generate_configuration_file(db_config, output_filename):
        j2_template_file = '3dCityDBImpExpConfig.j2'
        if not os.path.isfile(j2_template_file):
            logging.info(f'Jinja2 template file {j2_template_file} '
                        f'not found. Exiting')
            sys.exit(1)
        # Load template from file system
        template_loader = jinja2.FileSystemLoader(searchpath="./")
        template_env = jinja2.Environment(loader=template_loader)
        template = template_env.get_template(j2_template_file)
        # Create a TemplateStream object (that can be dumped into a file
        # afterwards) and replace the variables with the values from db_config
        template_stream = template.stream(PG_HOST=db_config['PG_HOST'],
                                          PG_PORT=db_config['PG_PORT'],
                                          PG_NAME=db_config['PG_NAME'],
                                          PG_USER=db_config['PG_USER'],
                                          PG_PASSWORD=db_config['PG_PASSWORD'])
        template_stream.dump(output_filename)

    def __init__(self):
        Demo.__init__(self)
        Demo.__init_databases__(self)
        for vintage in self.vintages:
            DemoLoad3DCityDB.generate_configuration_file(
                self.databases[vintage],
                DemoLoad3DCityDB.__get_vintage_configuration_filename(vintage))

    def run(self):
        input = self.get_input_demo()
        if not input.assert_output_files_exist():
            logging.error("DemoLoad3DCityDB misses some of its input files: exiting")
            sys.exit(1)
        self.create_output_dir()   # Just making sure

        for vintage in self.vintages:
            logging.info(f'Importation for vintage {str(vintage)}: starting.')
            d = DockerLoad3DCityDB()

            inputs = list(map(os.path.abspath, input.get_vintage_resulting_filenames(vintage)))
            d.set_files_to_import(inputs)
            logging.info(f'Files set for importation: {inputs}')

            d.set_configuration_filename(
                os.path.abspath(DemoLoad3DCityDB.__get_vintage_configuration_filename(vintage)))
            d.run()
            logging.info(f'Importation for vintage {str(vintage)}: done.')

if __name__ == '__main__':
    load = workflow.demo_load
    load.create_output_dir()

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=os.path.join(load.get_output_dir(),
                                              'demo_load_3dcitydb.log'),
                        filemode='w')

    logging.info('Stage 1: starting databases.')
    demo_servers = Demo3dCityDBServer()
    # FIXME: for some unknown reason the following line makes things go
    # wrong. Inquire on this only if you wish to rename the output directory name.
    # demo_servers.set_results_dir('data_bases')
    demo_servers.run()
    logging.info('Stage 1: waiting an extra 10 seconds for databases to spin off.')
    time.sleep(20)
    logging.info('Stage 1: done.')

    logging.info(f'Stage 2: importing files to databases.')
    load.run()
    logging.info('Stage 2: done')

    logging.info('Stage 3: halting containers.')
    demo_servers.halt()
    logging.info('Stage 3: done')
