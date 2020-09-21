import os
import sys
import logging
from abc import ABC, abstractmethod
from city_gml_files_from_archive import CityGMLFileFromArchive


class DemoLyonMetropoleDowloadAndSanitize(ABC):
    """
    Download some archives holding cityGML files
    """
    # FIXME: The following hard-wiring is a weakness
    patches_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                     '..',
                                     'Docker',
                                     'Collect-DockerContext',
                                     'DataPatches')

    @abstractmethod
    def define_archives(self):
        raise NotImplementedError()

    @abstractmethod
    def create_output_dir(self):
        raise NotImplementedError()

    def __init__(self, pattern):
        self.archives = dict()

        # Although the archive is spelled out the BATI string (which
        # stands for "constructed" in french) is holds a BATI cityGML
        # where BATI is here understood as building
        if pattern == 'BATI' or pattern == 'TIN' or \
           pattern == 'WATER' or pattern == 'PONT':
            self.pattern = pattern
        else:
            logging.info(f'Unknown pattern {pattern}. Exiting')
            sys.exit(1)

    def define_vintage_borough_archive(self, vintage, borough):
        repository = 'https://download.data.grandlyon.com/files/grandlyon/' \
                     'localisation/bati3d/'
        url = repository + borough + '_' + str(vintage) + '.zip'
        key_name = borough + '_' + str(vintage)
        filename = os.path.join(
            key_name,
            self.get_vintage_borough_output_file_basename(vintage, borough))
        self.archives[key_name] = CityGMLFileFromArchive(url=url,
                                                        name=filename,
                                                        year=vintage)

    def archives_to_sanitize(self):
        """Sanitizing files is the exception"""
        # Vintage 2009
        if 'LYON_4EME_2009' in self.archives:
            self.archives['LYON_4EME_2009']['old_name'] = 'LYON_4_BATI_2009.gml'
        if 'LYON_5EME_2009' in self.archives:
            self.archives['LYON_5EME_2009']['old_name'] = 'LYON_5_BATI_2009.gml'
        if 'LYON_7EME_2009' in self.archives:
            self.archives['LYON_7EME_2009']['patch_filename'] = \
              os.path.join(DemoLyonMetropoleDowloadAndSanitize.patches_directory,
                           'LYON_7EME_BATI_2009.gml.patch')
        if 'LYON_8EME_2009' in self.archives:
            self.archives['LYON_8EME_2009']['patch_filename'] = \
              os.path.join(DemoLyonMetropoleDowloadAndSanitize.patches_directory,
                           'LYON_8EME_BATI_2009.gml.patch')
        # Vintage 2012
        if 'LYON_7EME_2012' in self.archives:
            self.archives['LYON_7EME_2012']['patch_filename'] = \
              os.path.join(DemoLyonMetropoleDowloadAndSanitize.patches_directory,
                           'LYON_7EME_BATI_2012.gml.patch')
        if 'LYON_8EME_2012' in self.archives:
            self.archives['LYON_8EME_2012']['patch_filename'] = \
              os.path.join(DemoLyonMetropoleDowloadAndSanitize.patches_directory,
                           'LYON_8EME_BATI_2012.gml.patch')

        # Vintage 2015
        if 'LYON_7EME_2015' in self.archives:
            self.archives['LYON_7EME_2015']['old_name'] = 'LYON_7_BATI_2015.gml'

    def run(self):
        self.create_output_dir()   # Just making sure
        self.define_archives()
        self.archives_to_sanitize()
        # We only extract the buildings (BATI is a short batiment in
        # french which stands for buildings):
        for key_name, archive in self.archives.items():
            # Specify the target directory
            archive.set_directory(self.get_output_dir())
            archive.set_tidy_up()     # Comment out for debugging
            archive.download_and_expand(self.pattern)
            # It just happens that for the Grand Lyon zip files are expanded
            # they end up in a sub-directory having for name the key_name (but
            # this schema could be different for other data repositories that
            # build archives with another naming logic)
            # Note: this "knowledge" could be hidden away within the archive
            # object belonging class (because we could retrieve this
            # information out of the zip file). Nevertheless this renaming
            # is (awkwardly) placed in here in order to promote it to a higher
            # level in the class nesting on clarity purposes.
            archive.set_directory(os.path.join(archive.directory, key_name))
            archive.set_filename(os.path.basename(archive.get_filename()))
            archive.rename_when_needed()
            archive.patch_when_needed()
            archive.assert_file_exists()

    def get_vintage_borough_output_file_basename(self, vintage, borough):
        return borough + '_' + self.pattern + '_' + str(vintage) + '.gml'

    def get_resulting_filenames(self):
        result = list()
        for dummy, archive in self.archives.items():
            archive.assert_file_exists()    # Just making sure
            result.append(archive.get_full_filename())
        return result
