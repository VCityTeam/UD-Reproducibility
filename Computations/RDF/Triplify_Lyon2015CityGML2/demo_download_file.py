import os
import sys
import logging
import requests

class DemoDownloadFile:
    """
    A utility class for downloading a files.
    """
    def __init__(self):
        self.output_dir = None
        self.output_filename = None

    def set_output_dir(self, output_dir):
        self.output_dir = output_dir
        self.create_output_dir()

    def set_output_filename(self, output_filename):
        self.output_filename = output_filename

    def create_output_dir(self):
        full_output_dir_path = os.path.join(os.getcwd(), self.output_dir)
        if not os.path.isdir(full_output_dir_path):
            os.makedirs(full_output_dir_path)

    def download_file(self, url):
        self.assert_ready_for_run()
        request = requests.get(url)
        logging.info(f'http download status code: {request.status_code}')
        with open(f'{self.output_dir}/{self.output_filename}', 'wb') as file:
            file.write(request.content)

    def assert_ready_for_run(self):
        if self.output_dir is None:
            logging.error(f'No output_dir set. Exiting.')
            sys.exit(1)
        if self.output_filename is None:
            logging.error(f'No filename set. Exiting.')
            sys.exit(1)
