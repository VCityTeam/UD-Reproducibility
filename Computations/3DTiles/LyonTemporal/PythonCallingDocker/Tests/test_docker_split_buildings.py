import sys
import os
import logging
import pytest

sys.path.insert(0, '.')
from docker_split_buildings import DockerSplitBuilding, split

sys.path.insert(0, 'Tests')
from helper_test import md5


class TestDockerSplitBuilding:

    def shared(self):
        # We need to redirect DockerHelperBase loggers to standard output
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    @pytest.mark.run(order=4)
    def test_lyon_1er_2009_2012_split(self):
        self.shared()
        vintages = ['2009', '2012']
        out_files = []
        for vintage in vintages:
            in_out_dir = 'pytest_outputs/LYON_1ER_' + vintage
            in_filename = 'LYON_1ER_BATI_' + vintage + '.gml'
            out_filename = 'LYON_1ER_BATI_' + vintage + '_splited.gml'
            full_in_filename = os.path.join(in_out_dir, in_filename)
            full_out_filename = os.path.join(in_out_dir, out_filename)
            out_files.append(full_out_filename)

            if not os.path.isfile(full_in_filename):
                pytest.failt(f'Input file {full_in_filename} not found.')

            split(in_out_dir, in_filename, out_filename)

            if not os.path.isfile(full_out_filename):
                pytest.fail(f'Output file {full_out_filename} not found')

        if not md5(out_files[0]) == 'd4d40ba60cbbcedcb422d8afb92c6b3a':
            pytest.fail('Signature of ' + out_files[0] + ' does not match.')
        if not md5(out_files[1]) == '54d7520be48f594fa3d6e2169f53dd9a':
            pytest.fail('Signature of ' + out_files[1] + ' does not match.')
