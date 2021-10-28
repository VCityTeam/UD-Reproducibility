import os.path
import sys
import shutil
import logging
import yaml
from demo_static import DemoStatic
from demo_lyon_metropole_dowload_and_sanitize_static import (
    DemoLyonMetropoleDowloadAndSanitizeStatic,
)

kept_args = sys.argv[1:]  # The leading element is 'entrypoint.py'
# print("Container arguments: ", kept_args)
try:
    config = yaml.safe_load(kept_args[0])
    print(config)
except yaml.YAMLError as e:
    print(e)

DemoStatic(config).create_output_dir()
log_filename = os.path.join(
    DemoStatic(config).get_output_dir(), "demo_full_workflow.log"
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%a, %d %b %Y %H:%M:%S",
    filename=log_filename,
    filemode="w",
)
demo_download = DemoLyonMetropoleDowloadAndSanitizeStatic("BATI", "stage_1")
sys.exit(0)

logging.info("##################DemoFullWorkflow##### 1: Starting download.")
demo_download.run()
if not demo_download.assert_output_files_exist():
    logging.info("##################DemoFullWorkflow##### 1: Failed.")
    sys.exit(1)
logging.info("##################DemoFullWorkflow##### 1: Resulting files: ")
[logging.info("   " + file) for file in demo_download.get_resulting_filenames()]
logging.info("##################DemoFullWorkflow##### 1: Done.")

sys.exit(1)


if len(kept_args) == 0:
    # This was a request for the documentation (since no arguments).
    print("CityTiler (docker) expects at least two arguments :")
    print("  1. the Tiler to be applied: either Tiler or TemporalTiler")
    print("  2. the database server configuration file")
    print("When requesting the TemporalTiler ")
    print("  third to nth args: additionnal database servers configuration files,")
    print("  from n+1 to 2n+1 args: a time stamp (vintage) for each database.")
    print("Exiting.")
    sys.exit()

TilerMode = kept_args[0]
kept_args = kept_args[1:]
kept_args.pop(0)


if not os.path.isdir("junk"):
    shutil.copytree("junk", "/Output/TemporalTileset")

print("Exiting with success.")
