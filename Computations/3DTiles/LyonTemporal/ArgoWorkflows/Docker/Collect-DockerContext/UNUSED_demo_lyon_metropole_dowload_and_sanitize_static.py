import os
import sys
THIS FILE SHOULD NOT BE USED ANYMORE
from demo_static import DemoStatic, DemoWithFileOutputStatic

from demo_lyon_metropole_dowload_and_sanitize import DemoLyonMetropoleDowloadAndSanitize


class DemoLyonMetropoleDowloadAndSanitizeStatic(
    DemoWithFileOutputStatic, DemoLyonMetropoleDowloadAndSanitize
):
    def __init__(self, pattern, results_dir=None):
        # Because DemoWithFileOutputStatic inherits from DemoStatic but without
        # defining a constructor, we have to call the "grand-parent" constructor
        # directly (thus bypassing the un-existing parent constructor). This probably
        # reveal some conception problem...
        DemoStatic.__init__(self, results_dir)
        DemoLyonMetropoleDowloadAndSanitize.__init__(self, pattern)

    def define_archives(self):
        for borough in self.boroughs:
            self.define_vintage_borough_archive(self.vintage, borough)

    def get_resulting_filenames(self):
        return DemoLyonMetropoleDowloadAndSanitize.get_resulting_filenames(self)

    def get_borough_output_file_basename(self, borough):
        return DemoLyonMetropoleDowloadAndSanitize.get_vintage_borough_output_file_basename(
            self, self.vintage, borough
        )
