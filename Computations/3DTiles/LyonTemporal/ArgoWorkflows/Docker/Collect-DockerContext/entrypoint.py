import argparse
import logging
import os.path
import shutil
import sys
import yaml
import psutil

from lyon_metropole_dowload_and_sanitize import LyonMetropoleDowloadAndSanitize


def ParseCommandLine():
    # arg parse
    descr = """Download some Lyon Metropole CityGML files."""
    parser = argparse.ArgumentParser(description=descr)
    parser.add_argument(
        "--borough",
        nargs=1,
        type=str,
        required=True,
        help="Name of the borough to be retrieved.",
    )
    parser.add_argument(
        "--pattern",
        nargs=1,
        type=str,
        required=True,
        help="CityGML Modules in french (BATI...).",
    )
    parser.add_argument(
        "--results_dir",
        nargs=1,
        type=str,
        required=True,
        help="Name of the directory holding the results (reelative to persisted volume).",
    )
    parser.add_argument(
        "--vintage",
        nargs=1,
        type=str,
        required=True,
        help="Vintage to be retrieved (year among 2009, 2012, 2015).",
    )
    parser.add_argument(
        "--volume",
        nargs=1,
        type=str,
        required=True,
        help="Directory path of a persisted volume.",
    )

    return parser.parse_args()


def ReconstructInputParameters():
    cli_args = ParseCommandLine()
    print("Entrypoint: parsed arguments", cli_args)

    # The downstream code (using the input parameters) was written with the
    # assumption that it will handle over an object out of with that code will
    # extract each single parameter through the usage of the dot notation (
    # (that is <object>.attribute). Create an "empty object" (refer to
    # https://stackoverflow.com/questions/19476816/creating-an-empty-object-in-python )
    # and define its attributes
    parameters = type("", (), {})()

    parameters.borough = cli_args.borough[0]
    parameters.pattern = cli_args.pattern[0]
    parameters.vintage = cli_args.vintage[0]

    # Dealing with the outpur directory is a bit more cumbersome. We must first
    # assert that the persisted volume (for writing results) is properly
    # available within the container:
    persisted_output_dir = cli_args.volume[0]
    volume_present = set(
        filter(
            lambda x: str(x.mountpoint) == persisted_output_dir,
            psutil.disk_partitions(),
        )
    )
    if len(volume_present) == 1:
        print("The persisted volume ", persisted_output_dir, " is duly mounted")
    else:
        print(
            "The persisted volume directory ",
            persisted_output_dir,
            " does NOT seem to be properly mounted.",
        )
        # We must at least assert that the directory exists:
        if not os.path.isdir(persisted_output_dir):
            print("Unfound persisted volume directory: ", persisted_output_dir)
            print("Exiting")
            sys.exit(1)
        else:
            print("Yet the persisted volume directory seems to exist.")
            # Just to give some debug feedback by listing the files
            # Refer to
            # https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
            # for the one liner on listing files
            filenames = next(os.walk(persisted_output_dir), (None, None, []))[2]
            print("List of files within persisted volume directory: ", filenames)

    # Then, within the container, the configured results directory path must be
    # prepended with the persisted volume directory path.
    parameters.results_dir = os.path.join(persisted_output_dir, cli_args.results_dir[0])
    if not os.path.isdir(parameters.results_dir):
        os.makedirs(parameters.results_dir)
        if not os.path.isdir(parameters.results_dir):
            print("FAILED TO CREATE RESULTS DIR:", parameters.results_dir)
            sys.exit(1)
        else:
            print("Results dir: ", parameters.results_dir, "successfully created.")

    return parameters


parameters = ReconstructInputParameters()
print("Entrypoint parameters: ", vars(parameters))

log_filename = os.path.join(parameters.results_dir, "Download_And_Sanitize.log")
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%a, %d %b %Y %H:%M:%S",
    filename=log_filename,
    filemode="w",
)

download = LyonMetropoleDowloadAndSanitize(parameters)

logging.info("##################DemoFullWorkflow##### 1: Starting download.")
download.run()
if not download.assert_output_files_exist():
    logging.info("##################DemoFullWorkflow##### 1: Failed.")
    sys.exit(1)
logging.info("##################DemoFullWorkflow##### 1: Resulting files: ")
[logging.info("   " + file) for file in download.get_resulting_filenames()]
with open(os.path.join(parameters.results_dir, "Resulting_Filenames.txt"), "a+") as f:
    [f.write(file + "\n") for file in download.get_resulting_filenames()]
logging.info("##################DemoFullWorkflow##### 1: Done.")

print("Exiting with success.")
