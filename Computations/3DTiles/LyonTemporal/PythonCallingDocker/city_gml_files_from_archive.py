import os
import re
import sys
import zipfile
import patch
import shutil
import logging
import wget
from pushd import pushd


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
        # The directory where the extracted cityGML file ends up located
        self.output_directory = None
        # Weather of not we should remove un-required/temporary files
        # (like the original archive) in the sake of disk space.
        self.tidy_up = False

    def __setitem__(self, key, val):
        if key not in CityGMLFileFromArchive._keys:
            logging.info(f'CityGMLFileFromArchive: forbidden key: {key}')
            raise KeyError
        dict.__setitem__(self, key, val)

    def set_output_directory(self, directory):
        self.output_directory = directory
        if not os.path.isdir(self.output_directory):
            os.makedirs(self.output_directory)

    def get_output_directory(self):
        return self.output_directory

    def set_tidy_up(self):
        self.tidy_up = True

    def set_filename(self, name):
        self['name'] = name

    def get_filename(self):
        return self['name']

    def get_full_filename(self):
        """Fully qualified pathname for the file"""
        return os.path.join(self.get_output_directory(), self['name'])

    def assert_directory_is_set(self):
        if not self.get_output_directory():
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
        with pushd(self.get_output_directory()):
            # Because the server/network are sometimes flaky, giving many tries might
            # robustify the process:
            download_success = False
            number_max_wget_trial = 5
            seeked_url = self['url']
            while not download_success:
                try:
                    wget.download(seeked_url)
                    download_success = True
                    logging.info(f'Download of {seeked_url} succeful.')
                except:
                    number_max_wget_trial -=1
                    if number_max_wget_trial:
                        logging.info(f'Download of {seeked_url} failed: retying.')
                    else:
                        logging.info(f'Download of {seeked_url} failed: exiting.')
                        sys.exit(1)

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
        old = os.path.join(self.get_output_directory(), self['old_name'])
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
            self.get_output_directory(), os.path.basename(self['patch_filename']))
        shutil.copyfile(source_patch, target_patch_file)
        patch_file = os.path.basename(source_patch)
        with pushd(self.get_output_directory()):
            try:
                success = patch.fromfile(patch_file).apply()
            except:
                success = False
            if not success:
                logging.info(f'Patch failed for {source_patch}. Exiting')
                sys.exit(1)
