import os
import sys
import logging
import jinja2
import time

from docker_load_3dcitydb import DockerLoad3DCityDB
from demo_3dcitydb_server import Demo3dCityDBServer
from demo_strip_attributes import DemoStrip
from demo import Demo


class DemoLoad3DCityDB(Demo):
    
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
        for vintage in self.vintages:
            logging.info(f'Importation for vintage {str(vintage)}: starting.')
            d = DockerLoad3DCityDB()

            inputs = list(map(os.path.abspath, 
                              DemoStrip().get_vintage_resulting_filenames(vintage)))
            d.set_files_to_import(inputs)
            logging.info(f'Files set for importation: {inputs}')

            d.set_configuration_filename(
                os.path.abspath(DemoLoad3DCityDB.__get_vintage_configuration_filename(vintage)))
            d.run()
            logging.info(f'Importation for vintage {str(vintage)}: done.')

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # Note: there is probably something simpler to be done with
    # LyonMetropoleDowloadAndSanitize.get_resulting_filenanes() but we
    # cannot access it in this context

    logging.info('Stage 1: starting databases.')
    demo_servers = Demo3dCityDBServer()
    demo_servers.run()
    logging.info('Stage 1: waiting an extra 10 seconds for databases to spin off.')
    time.sleep(20)
    logging.info('Stage 1: done.')

    logging.info(f'Stage 2: importing files to databases.')
    demo_load = DemoLoad3DCityDB()
    demo_load.run()
    logging.info('Stage 2: done')

    logging.info('Stage 3: halting containers.')
    # demo_servers.halt()
    logging.info('Stage 3: done')
