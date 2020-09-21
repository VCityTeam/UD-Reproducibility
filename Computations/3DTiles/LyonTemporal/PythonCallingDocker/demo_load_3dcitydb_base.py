import os
import sys
import logging
import jinja2

class DemoLoad3DCityDBBase:

    @staticmethod
    def generate_configuration_file(db_config, output_filename):
        """
        The 3dCityDB-importer requires a configuration with an ad-hoc (xml format) 
        file that must be generated out of the demo_configuration file.  
        """
        this_file_dir = os.path.dirname(os.path.realpath(__file__))
        # j2_template_file = os.path.join(this_file_dir, '3dCityDBImpExpConfig.j2')
        j2_template_file = '3dCityDBImpExpConfig.j2'

        if not os.path.isfile(os.path.join(this_file_dir, j2_template_file)):
            logging.info(f'Jinja2 template file {j2_template_file} not found. Exiting')
            sys.exit(1)

        # Load template from file system
        template_loader = jinja2.FileSystemLoader(searchpath=[this_file_dir])

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

