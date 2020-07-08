import sys
import os
import unittest
import logging
import pytest
from docker_strip_attributes import DockerStripAttributes
from helper_test import md5

sys.path.insert(0, '.')
sys.path.insert(0, 'Tests')


class TestDockerStripAttributes(unittest.TestCase):

    def shared(self):
        # We need to redirect DockerHelper loggers to# standard output
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    def test_lyon_1er_2009_strip(self):
        self.shared()

        in_out_dir = 'junk/LYON_1ER_2009'
        in_filename = 'LYON_1ER_BATI_2009_splited.gml'
        out_filename = 'LYON_1ER_BATI_2009_splited_stripped.gml'
        full_in_filename = os.path.join(in_out_dir, in_filename)
        full_out_filename = os.path.join(in_out_dir, out_filename)

        if not os.path.isfile(full_in_filename):
            print(f'Input file {full_in_filename} not found.')
            self.fail()

        d = DockerStripAttributes()
        d.set_mounted_input_directory(os.path.join(os.getcwd(), in_out_dir))
        d.set_mounted_output_directory(d.get_mounted_input_directory())
        d.set_input_filename(in_filename)
        d.set_output_filename(out_filename)
        d.run()

        if not os.path.isfile(full_out_filename):
            self.fail()
        if not md5(full_out_filename) == 'd4d40ba60cbbcedcb422d8afb92c6b3a':
            self.fail()