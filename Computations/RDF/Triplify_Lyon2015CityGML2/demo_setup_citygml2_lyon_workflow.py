import os
import sys
import logging
import shutil
from git import Repo
from demo_download_file import DemoDownloadFile

class DemoSetupCityGML2Lyon():
    """
    Download and setup CityGML 3.0 transformation pipeline
    """
    def __init__(self):
        self.data_dir = 'demo_data/'
        # shapechange stage
        self.stage1_dir = f'{self.data_dir}stage1/'
        # ontology linking stage
        self.stage2_dir = f'{self.data_dir}stage2/'
        # gml to graph transformation stage
        self.stage3_dir = f'{self.data_dir}stage3/'
        # final output directory
        self.demo_output_dir = f'{self.data_dir}output/'
        # ud-graph docker context directory
        self.context_dir = 'UD-Graph-docker'
        if not os.path.isdir(self.context_dir):
            self.create_docker_context()

        # filenames and directories
        self.local_files_dir = 'DemoCityGML2Lyon2015'
        self.shapechange_config_filename = 'CityGML2.0_config.xml'
        self.citygml_uml_filename = 'CityGML_2.0_Conceptual_Model.xml'
        self.citygml_owl_dir = 'CityGML_2.0_Ontology'
        self.geosparql_owl_filename = 'geosparql_vocab_all.rdf'
        self.geosparql_owl_uri = 'http://www.opengis.net/ont/geosparql#'
        self.gml_owl_filename = 'gml_32_geometries.rdf'
        self.gml_owl_uri = 'http://www.opengis.net/ont/gml#'
        self.citygml_data_filename = 'LYON_1ER_BATI_2015-1_bldg-patched.gml'
        self.iso19136_dir = 'iso19136'

    def create_dir(self, dir):
        full_dir_path = os.path.join(os.getcwd(), dir)
        if not os.path.isdir(full_dir_path):
            os.makedirs(full_dir_path)

    def create_docker_context(self):
        Repo.clone_from('https://github.com/VCityTeam/UD-Graph-docker.git', self.context_dir)

    def setup_demo(self):
        downloader = DemoDownloadFile()
        # create input/output folders
        self.create_dir(self.stage1_dir)
        self.create_dir(self.stage2_dir)
        self.create_dir(self.stage3_dir)
        self.create_dir(self.demo_output_dir)
        # prepare stage 1 - shapechange
        full_local_filename = os.path.join(os.getcwd(),
                                           self.local_files_dir,
                                           self.shapechange_config_filename)
        full_input_filename = os.path.join(os.getcwd(),
                                           self.stage1_dir,
                                           self.shapechange_config_filename)
        shutil.copyfile(full_local_filename, full_input_filename)

        full_local_filename = os.path.join(os.getcwd(),
                                           self.local_files_dir,
                                           self.citygml_uml_filename)
        full_input_filename = os.path.join(os.getcwd(),
                                           self.stage1_dir,
                                           self.citygml_uml_filename)
        shutil.copyfile(full_local_filename, full_input_filename)
        # prepare stage 2 - ontology linking
        # TODO: add ontology linking stage to calculation
        # prepare stage 3 - gml to graph transformation
        downloader.set_output_dir(self.stage3_dir)
        downloader.set_output_filename(self.geosparql_owl_filename)
        downloader.download_file(self.geosparql_owl_uri)
        downloader.set_output_filename(self.gml_owl_filename)
        downloader.download_file(self.gml_owl_uri)
        full_local_filename = os.path.join(os.getcwd(),
                                           self.local_files_dir,
                                           self.citygml_data_filename)
        full_input_filename = os.path.join(os.getcwd(),
                                           self.stage3_dir,
                                           self.citygml_data_filename)
        shutil.copyfile(full_local_filename, full_input_filename)
        full_local_dir = os.path.join(os.getcwd(),
                                      self.local_files_dir,
                                      self.iso19136_dir)
        full_input_dir = os.path.join(os.getcwd(),
                                      self.stage3_dir,
                                      self.iso19136_dir)
        shutil.copytree(full_local_dir, full_input_dir)

    def clean(self):
        full_data_dir_path = os.path.join(os.getcwd(), self.data_dir)
        if os.path.isdir(full_data_dir_path):
            shutil.rmtree(full_data_dir_path)

    def assert_stages_ready_for_run(self):
        ### verify stage 1 ###
        full_dir_path = os.path.join(os.getcwd(), self.stage1_dir)
        if not os.path.isdir(full_dir_path):
            logging.error(f'Directory {full_dir_path} not found. Exiting.')
            sys.exit(1)
        full_file_path = os.path.join(os.getcwd(),
                                      self.stage1_dir,
                                      self.shapechange_config_filename)
        if not os.path.isfile(full_file_path):
            logging.error(f'File {full_file_path} not found. Exiting.')
            sys.exit(1)
        full_file_path = os.path.join(os.getcwd(),
                                      self.stage1_dir,
                                      self.citygml_uml_filename)
        if not os.path.isfile(full_file_path):
            logging.error(f'File {full_file_path} not found. Exiting.')
            sys.exit(1)
        ### verify stage 2 ###
        full_dir_path = os.path.join(os.getcwd(), self.stage2_dir)
        if not os.path.isdir(full_dir_path):
            logging.error(f'Directory {full_dir_path} not found. Exiting.')
            sys.exit(1)
        ### verify stage 3 ###
        full_dir_path = os.path.join(os.getcwd(), self.stage3_dir)
        if not os.path.isdir(full_dir_path):
            logging.error(f'Directory {full_dir_path} not found. Exiting.')
            sys.exit(1)
        full_file_path = os.path.join(os.getcwd(),
                                      self.stage3_dir,
                                      self.geosparql_owl_filename)
        if not os.path.isfile(full_file_path):
            logging.error(f'File {full_file_path} not found. Exiting.')
            sys.exit(1)
        full_file_path = os.path.join(os.getcwd(),
                                      self.stage3_dir,
                                      self.gml_owl_filename)
        if not os.path.isfile(full_file_path):
            logging.error(f'File {full_file_path} not found. Exiting.')
            sys.exit(1)
        ### verify output ###
        full_dir_path = os.path.join(os.getcwd(), self.demo_output_dir)
        if not os.path.isdir(full_dir_path):
            logging.error(f'Directory {full_dir_path} not found. Exiting.')
            sys.exit(1)
