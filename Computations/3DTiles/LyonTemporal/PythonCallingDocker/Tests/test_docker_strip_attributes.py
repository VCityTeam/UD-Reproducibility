import sys
import os
import logging
import pytest

sys.path.insert(0, '.')
from docker_strip_attributes import DockerStripAttributes
from demo_strip_attributes import StripInputsOutputs

sys.path.insert(0, 'Tests')
from helper_test import md5


class TestDockerStripAttributes:

    def shared(self):
        # We need to redirect DockerHelperBase loggers to standard output
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    # The following usage of mark.dependency produces the test to be skipped
    # (even when the script it depends on ran smoothly). It seems that
    # whatever the name of the test (on which this one depends) might be
    # (e.g. "aaaaaaaaaaaa" that doesn't exist), the result is the same:
    # this test is skipped...
    # @pytest.mark.dependency(
    #    depends=["tests/test_lyon_metropole_dowload_and_sanitize.py::TestLyonMetropoleDowloadAndSanitize::test_lyon_1er_2009"],
    #    scope='session')
    #
    # Getting the following ordering to be respected also failed (both versions)
    # @pytest.mark.run(after='tests/test_lyon_metropole_dowload_and_sanitize.py::TestLyonMetropoleDowloadAndSanitize::test_lyon_1er_2009')
    # @pytest.mark.run(after='test_lyon_1er_2009')
    #
    @pytest.mark.run(order=5)
    def test_lyon_1er_2009_2012_strip(self):
        self.shared()

        vintages = ['2009', '2012']
        stripper = StripInputsOutputs()
        out_files = []

        for vintage in vintages:
            in_out_dir = 'pytest_outputs/LYON_1ER_' + vintage
            in_filename = 'LYON_1ER_BATI_' + vintage + '_splited.gml'
            out_filename = 'LYON_1ER_BATI_' + vintage + '_splited_stripped.gml'
            full_in_filename = os.path.join(in_out_dir, in_filename)
            full_out_filename = os.path.join(in_out_dir, out_filename)
            out_files.append(full_out_filename)

            if not os.path.isfile(full_in_filename):
                pytest.fail(f'Input file {full_in_filename} not found.')

            stripper.strip_single_file(
                DockerStripAttributes(),
                input_dir=in_out_dir,
                input_filename=in_filename,
                output_dir=in_out_dir
            )

            if not os.path.isfile(full_out_filename):
                pytest.fail(f'Output file {full_out_filename} not found.')

        if not md5(out_files[0]) == '9a05e075b8e08491adea1255c55ea26a':
            pytest.fail('Signature of ' + out_files[0] + ' does not match.')
        if not md5(out_files[1]) == 'b508e21e5c77c15e0c6c404ead69555e':
            pytest.fail('Signature of ' + out_files[1] + ' does not match.')
