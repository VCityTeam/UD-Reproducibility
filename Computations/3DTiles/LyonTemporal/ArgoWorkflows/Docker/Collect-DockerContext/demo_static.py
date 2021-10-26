import os
from abc import ABC, abstractmethod
from demo import Demo, DemoWithFileOutput


# CLEANME import demo_configuration_static
class DemoStatic(Demo):
    def __init__(self, vintage, results_dir, all_demos_output_dir, city, boroughs):
        super().__init__(results_dir, all_demos_output_dir, city, boroughs)
        self.vintage = vintage


class DemoWithFileOutputStatic(DemoStatic, DemoWithFileOutput, ABC):
    """
    Additionnal conventions structuring the file layout
    """

    @abstractmethod
    def get_borough_output_file_basename(self, borough):
        raise NotImplementedError()

    def get_borough_output_directory_name(self, borough):
        return os.path.join(self.get_output_dir(), borough + "_" + str(self.vintage))

    def get_borough_output_filename(self, borough):
        """
        :return: the filename for the given borough as layed out after the
                 download and patch. This function result DOES include the directory
                 name in which the output file lies.
        """
        return os.path.join(
            self.get_borough_output_directory_name(borough),
            self.get_borough_output_file_basename(borough),
        )
