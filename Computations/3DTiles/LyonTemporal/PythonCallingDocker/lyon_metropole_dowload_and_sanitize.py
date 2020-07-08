import os
import re
import sys
import zipfile
import patch
import shutil
import logging
import wget
from pushd import pushd
import demo_configuration as demo


class CityGMLFileFromArchive(dict):

    _keys = "url name patch_filename old_name vintage".split()
    # url: the url where to retrieve the archive from
    # name: the name of the cityGML file this class retrieves and
    #       sanitizes
    # old_name: the name of the cityGML as it got extracted from the archive
    #           (and miss-named).
    # patch_filename: the patch that should optionnally be applied
    # vintage: the year (as integer) at which the file corresponds to

    # Technical reference: 'https://treyhunner.com/2019/04/'\
    #            'why-you-shouldnt-inherit-from-list-and-dict-in-python/'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # The directory where the cityGML file ends up located
        self.directory = None
        # Weather of not we should remove un-required/temporary files
        # (like the original archive) in the sake of disk space.a
        self.tidy_up = False

    def __setitem__(self, key, val):
        if key not in CityGMLFileFromArchive._keys:
            logging.info(f'CityGMLFileFromArchive: forbidden key: {key}')
            raise KeyError
        dict.__setitem__(self, key, val)

    def set_directory(self, directory):
        self.directory = directory
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)

    def get_directory(self):
        return self.directory

    def set_tidy_up(self):
        self.tidy_up = True

    def set_filename(self, name):
        self['name'] = name

    def get_filename(self):
        return self['name']

    def get_full_filename(self):
        """Fully qualified pathname for the file"""
        return os.path.join(self.directory, self['name'])

    def assert_directory_is_set(self):
        if not self.directory:
            logging.info('CityGMLFileFromArchive: unset directory. Exiting.')
            sys.exit(1)

    def assert_file_exists(self):
        if 'name' not in self:
            logging.info('CityGMLFileFromArchive: unset name. Exiting.')
            sys.exit(1)
        full_filename = self.get_full_filename()
        if not os.path.isfile(full_filename):
            logging.info(f'Extracted file {full_filename} not found. Exiting.')
            sys.exit(1)

    def download_and_expand(self, pattern):
        self.assert_directory_is_set()
        with pushd(self.directory):
            wget.download(self['url'])
            downloaded = os.path.basename(super().get('url'))
            with zipfile.ZipFile(downloaded, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    if re.search(pattern, file):
                        zip_ref.extract(file)
            if self.tidy_up:
                os.remove(downloaded)
        # Note: we cannot yet assert_file_exists() because some renaming
        # might be required.

    def rename_when_needed(self):
        self.assert_directory_is_set()
        if 'old_name' not in self:
            return
        if 'name' not in self:
            logging.info('CityGMLFileFromArchive: unset name. Exiting.')
            sys.exit(1)
        old = os.path.join(self.directory, self['old_name'])
        if not os.path.isfile(old):
            logging.info(f'File to rename {old} not found. Exiting')
            sys.exit(1)
        os.rename(old, self.get_full_filename())
        self.assert_file_exists()

    def patch_when_needed(self):
        self.assert_directory_is_set()
        if 'patch_filename' not in self:
            return
        # Because patch files are relative (they refer to the file to which
        # the patch is applied by including this name in the patch), we first
        # need to copy the patch locally (i.e. in self.directory)
        source_patch = self['patch_filename']
        if not os.path.isfile(source_patch):
            logging.info(f'Patch file {source_patch} not found. Exiting')
            sys.exit(1)
        target_patch_file = os.path.join(
            self.directory, os.path.basename(self['patch_filename']))
        shutil.copyfile(source_patch, target_patch_file)
        patch_file = os.path.basename(source_patch)
        with pushd(self.directory):
            try:
                success = patch.fromfile(patch_file).apply()
            except:
                success = False
            if not success:
                logging.info(f'Patch failed for {source_patch}. Exiting')
                sys.exit(1)


class LyonMetropoleDowloadAndSanitize:
    """
    Download some archives holding cityGML files
    """
    # FIXME: The following hard-wiring is a weakness
    patches_directory = '../Docker/Collect-DockerContext/DataPatches'

    def __init__(self, vintages, boroughs, pattern):
        self.archives = dict()
        self.target_directory = os.getcwd()
        self.vintages = vintages
        self.boroughs = boroughs

        # Although the archive is spelled out the BATI string (which
        # stands for "constructed" in french) is holds a BATI cityGML
        # where BATI is here understood as building
        if pattern == 'BATI' or pattern == 'TIN' or \
           pattern == 'WATER' or pattern == 'PONT':
            self.pattern = pattern
        else:
            logging.info(f'Unknown pattern {pattern}. Exiting')
            sys.exit(1)

    def set_output_directory(self, target_directory):
        self.target_directory = target_directory

    def define_archives(self):
        for year in self.vintages:
            for borough in self.boroughs:
                repository = 'https://download.data.grandlyon.com/files/' \
                             'grandlyon/localisation/bati3d/'
                url = repository + borough + '_' + str(year) + '.zip'
                key_name = borough + '_' + str(year)
                # "BATI" refers here to the name of the archive as opposed
                # to building (refer to self.pattern variable documentation)
                filename = os.path.join(key_name,
                                        borough + '_BATI_' + str(year) + '.gml')
                self.archives[key_name] = CityGMLFileFromArchive(url=url,
                                                                 name=filename,
                                                                 year=year)

    def archives_to_sanitize(self):
        """Sanitizing files is the exception"""
        # Vintage 2009
        if 'LYON_4EME_2009' in self.archives:
            self.archives['LYON_4EME_2009']['old_name'] = 'LYON_4_BATI_2009.gml'
        if 'LYON_5EME_2009' in self.archives:
            self.archives['LYON_5EME_2009']['old_name'] = 'LYON_5_BATI_2009.gml'
        if 'LYON_7EME_2009' in self.archives:
            self.archives['LYON_7EME_2009']['patch_filename'] = \
              os.path.join(LyonMetropoleDowloadAndSanitize.patches_directory,
                           'LYON_7EME_BATI_2009.gml.patch')
        if 'LYON_8EME_2009' in self.archives:
            self.archives['LYON_8EME_2009']['patch_filename'] = \
              os.path.join(LyonMetropoleDowloadAndSanitize.patches_directory,
                           'LYON_8EME_BATI_2009.gml.patch')
        # Vintage 2012
        if 'LYON_7EME_2012' in self.archives:
            self.archives['LYON_7EME_2012']['patch_filename'] = \
              os.path.join(LyonMetropoleDowloadAndSanitize.patches_directory,
                           'LYON_7EME_BATI_2012.gml.patch')
        if 'LYON_8EME_2012' in self.archives:
            self.archives['LYON_8EME_2012']['patch_filename'] = \
              os.path.join(LyonMetropoleDowloadAndSanitize.patches_directory,
                           'LYON_8EME_BATI_2012.gml.patch')

        # Vintage 2015
        if 'LYON_7EME_2015' in self.archives:
            self.archives['LYON_7EME_2015']['old_name'] = 'LYON_7_BATI_2015.gml'

    def run(self):
        self.define_archives()
        self.archives_to_sanitize()
        # We only extract the buildings (BATI is a short batiment in
        # french which stands for buildings):
        for key_name, archive in self.archives.items():
            # Specify the target directory
            archive.set_directory(self.target_directory)
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

    def get_resulting_filenanes(self):
        result = list()
        for dummy, archive in self.archives.items():
            archive.assert_file_exists()    # Just making sure
            result.append(archive.get_full_filename())
        return result


if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='lyon_metropole_dowload_and_sanitize.log',
                        filemode='w')

    d = LyonMetropoleDowloadAndSanitize(demo.vintages, demo.boroughs, 'BATI')
    d.set_output_directory(demo.output_dir)
    d.run()
    print("Resulting files: ")
    for f in d.get_resulting_filenanes():
        print(f)
