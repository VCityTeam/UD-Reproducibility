import os
import sys
import logging
import shutil
from demo_setup_citygml2_lyon_workflow import DemoSetupCityGML2Lyon
from docker_xml2rdf import DockerXML2RDF
from docker_shapechange import DockerShapechange

if __name__ == "__main__":

    sys.path.append('../')
    log_filename = os.path.join(os.getcwd(), 'run_citygml2_lyon_workflow.log')

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename=log_filename,
                        filemode='w')

    ### Setup stages ###
    print('Setting up demo...')
    demo = DemoSetupCityGML2Lyon()
    demo.clean()
    demo.setup_demo()
    demo.assert_stages_ready_for_run()

    ### Stage 1: Transform CityGML 2.0 conceptual model to OWL ###
    print('Demo setup complete. Begin Stage 1...')
    DockerShapechange.transform_single_file(demo.stage1_dir,
                                            demo.citygml_uml_filename,
                                            demo.citygml_owl_dir,
                                            demo.shapechange_config_filename)

    ### Stage 2: Transform CityGML dataset into RDF ###
    print('Stage 1 complete. Begin Stage 2...')
    stage1_output = os.path.join(demo.stage1_dir, demo.citygml_owl_dir)
    stage2_input = os.path.join(demo.stage2_dir, demo.citygml_owl_dir)
    shutil.copytree(stage1_output, stage2_input)

    DockerXML2RDF.transform_single_file(demo.stage2_dir,
                                        demo.citygml_data_filename,
                                        demo.citygml_owl_dir,
                                        demo.xml2rdf_config)
    print('Stage 2 complete. Workflow complete!')
