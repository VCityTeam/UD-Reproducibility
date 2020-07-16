import sys
import os
import logging
import pytest
import time

sys.path.insert(0, '.')
from docker_strip_attributes import DockerStripAttributes

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
    @pytest.mark.run(order=3)
    def test_lyon_1er_2009_strip(self):
        self.shared()

        in_out_dir = 'pytest_outputs/LYON_1ER_2009'
        in_filename = 'LYON_1ER_BATI_2009_splited.gml'
        out_filename = 'LYON_1ER_BATI_2009_splited_stripped.gml'
        full_in_filename = os.path.join(in_out_dir, in_filename)
        full_out_filename = os.path.join(in_out_dir, out_filename)

        if not os.path.isfile(full_in_filename):
            pytest.fail(f'Input file {full_in_filename} not found.')

        d = DockerStripAttributes()
        d.set_mounted_input_directory(os.path.join(os.getcwd(), in_out_dir))
        d.set_mounted_output_directory(d.get_mounted_input_directory())
        d.set_input_filename(in_filename)
        d.set_output_filename(out_filename)
        d.run()

        # Because of caching issues for bind mounts on OSX, refer e.g. to
        # https://docs.docker.com/docker-for-mac/osxfs-caching/
        # the following check sometimes fails (although the file will
        # eventually "pop up" when the buffers get processed). We thus
        # introduce the following delay kludge:
        time.sleep(10)

        if not os.path.isfile(full_out_filename):
            pytest.fail(f'Output file {full_out_filename} not found.')
        if not md5(full_out_filename) == '9a05e075b8e08491adea1255c55ea26a':
            pytest.fail('Signature of outfile does not match.')
