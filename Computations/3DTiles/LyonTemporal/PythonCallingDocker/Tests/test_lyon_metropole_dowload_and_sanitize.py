import sys
import unittest

sys.path.insert(0, '.')
from lyon_metropole_dowload_and_sanitize import *

sys.path.insert(0, 'Tests')
from helper_test import md5


class TestLyonMetropoleDowloadAndSanitize(unittest.TestCase):

    def shared(self):
        # We need to redirect LyonMetropoleDowloadAndSanitize loggers to
        # standard output
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
  
    def test_lyon_1er_2009(self):
        """
        This is the vanilla case i.e. download and expand the zip file
        without further ado (like renaming files, applying patches)...
        """
        self.shared()
        loader = LyonMetropoleDowloadAndSanitize([2009], ['LYON_1ER'], 'BATI')
        loader.set_output_directory('pytest_outputs')
        loader.run()
        files = loader.get_resulting_filenanes()
        if not len(files) == 1:
            self.fail()
        if not md5(files[0]) == 'ce21b88136f30ffe888c3e859b92306c':
            self.fail()

    def test_lyon_4eme_2009(self):
        """
        This care imposes the renaming of the extracted files.
        """
        # We need to redirect LyonMetropoleDowloadAndSanitize loggers to
        # standard output
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

        loader = LyonMetropoleDowloadAndSanitize([2009], ['LYON_4EME'], 'BATI')
        loader.set_output_directory('pytest_outputs')
        loader.run()
        files = loader.get_resulting_filenanes()
        if not len(files) == 1:
            self.fail()
        if not md5(files[0]) == '3c087e0064d284a5f852d2fcd4c73497':
            self.fail()

    def test_lyon_7eme_2009(self):
        """
        This case illustrates the application of patch.
        """
        self.shared()
        loader = LyonMetropoleDowloadAndSanitize([2009], ['LYON_7EME'], 'BATI')
        loader.set_output_directory('pytest_outputs')
        loader.run()
        files = loader.get_resulting_filenanes()
        if not len(files) == 1:
            self.fail()
        if not md5(files[0]) == 'a9050aed7b48935068b608c481cb84f5':
            self.fail()
