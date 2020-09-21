import os
import sys
import logging
from demo_temporal import DemoTemporal, DemoWithFileOutputTemporal

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from demo_lyon_metropole_dowload_and_sanitize import DemoLyonMetropoleDowloadAndSanitize


class DemoLyonMetropoleDowloadAndSanitizeTemporal(DemoWithFileOutputTemporal,
                                                  DemoLyonMetropoleDowloadAndSanitize):

    def __init__(self, pattern, results_dir=None):
        # Because DemoWithFileOutputTemporal inherits from DemoTemporal but without
        # defining a constructor, we have to call the "grand-parent" constructor
        # directly (thus bypassing the un-existing parent constructor). This probably
        # reveal some conception problem...
        DemoTemporal.__init__(self, results_dir)
        DemoLyonMetropoleDowloadAndSanitize.__init__(self, pattern)

    def define_archives(self):
        for vintage in self.vintages:
            for borough in self.boroughs:
                self.define_vintage_borough_archive(vintage, borough)

    def get_resulting_filenames(self):
        return  DemoLyonMetropoleDowloadAndSanitize.get_resulting_filenames(self)

    def get_vintage_borough_output_file_basename(self, vintage, borough):
        return (DemoLyonMetropoleDowloadAndSanitize
                .get_vintage_borough_output_file_basename(self, vintage, borough))
   


