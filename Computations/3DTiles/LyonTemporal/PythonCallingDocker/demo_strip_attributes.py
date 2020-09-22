import os

class DemoStrip:
    """
    A utility class gathering the conventional names, relative to this demo,
    used by the strip algorithms for designating its input/output directories
    and filenames
    """
    
    @staticmethod
    def derive_output_file_basename_from_input(input_filename):
        input_filename = os.path.basename(input_filename)
        input_no_extension = input_filename.rsplit('.', 1)[0]
        return input_no_extension + '_stripped.gml'
