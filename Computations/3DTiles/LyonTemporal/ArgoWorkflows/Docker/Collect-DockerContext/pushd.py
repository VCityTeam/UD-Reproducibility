# Taken from https://stackoverflow.com/questions/6194499/pushd-through-os-system
import os
import contextlib


@contextlib.contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    try:
        os.chdir(new_dir)
    except:
        logging.error(f'Could not push to directory {new_dir}')
        files = [f for f in os.listdir('.') if os.path.isfile(f)]
        logging.error(f'Files in current directory {files}')
        logging.error('Exiting')
        sys.exit(1)
    yield
    os.chdir(previous_dir)
