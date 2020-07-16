import sys
import os
import logging
import pytest

sys.path.insert(0, '.')
from docker_split_buildings import DockerSplitBuilding

sys.path.insert(0, 'Tests')
from helper_test import md5


class TestDockerSplitBuilding:

    def shared(self):
        # We need to redirect DockerHelperBase loggers to standard output
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    @pytest.mark.run(order=2)
    def test_lyon_1er_2009_split(self):
        self.shared()

        in_out_dir = 'pytest_outputs/LYON_1ER_2009'
        in_filename = 'LYON_1ER_BATI_2009.gml'
        out_filename = 'LYON_1ER_BATI_2009_splited.gml'
        full_in_filename = os.path.join(in_out_dir, in_filename)
        full_out_filename = os.path.join(in_out_dir, out_filename)

        if not os.path.isfile(full_in_filename):
            pytest.failt(f'Input file {full_in_filename} not found.')

        d = DockerSplitBuilding()
        d.set_mounted_input_directory(os.path.join(os.getcwd(), in_out_dir))
        d.set_mounted_output_directory(d.get_mounted_input_directory())
        d.set_input_filename(in_filename)
        d.set_output_filename(out_filename)
        d.run()

        if not os.path.isfile(full_out_filename):
            pytest.fail(f'Output file {full_out_filename} not found')
        if not md5(full_out_filename) == 'd4d40ba60cbbcedcb422d8afb92c6b3a':
            pytest.fail('Signature of outfile does not match.')

