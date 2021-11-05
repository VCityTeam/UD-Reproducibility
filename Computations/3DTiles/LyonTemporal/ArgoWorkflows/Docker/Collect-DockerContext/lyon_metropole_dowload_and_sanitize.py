import os
import sys
import logging
from city_gml_files_from_archive import CityGMLFileFromArchive


class LyonMetropoleDowloadAndSanitize:
    """
    Download some archives holding cityGML files
    """

    # FIXME: The following hard-wiring is a weakness
    patches_directory = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..",
        "Docker",
        "Collect-DockerContext",
        "DataPatches",
    )

    def __init__(self, parameters):
        # results_dir designates the directory where all  outputs/results
        # will be located:
        self.results_dir = parameters.results_dir
        # FIXME self.city = city
        self.borough = parameters.borough
        self.vintage = parameters.vintage

        # This class only download a single archive. Yet some archives (as
        # gotten from LyonMetropole) required to be pacthed/fixed. The structure
        # of the following code is imported from previous versions where the
        # logic of this class was to iterate on all the archives to download.
        # This was the reason for self.archiveS. Now, because we had a
        # dictionnary of archives to download, it was natural to attach to
        # the same structure the infomation required for the patches (refer
        # to register_archives_to_sanitize()). But within this new context
        # of a single archive to download we do not need to loop on
        # self.archives: yet we keep this structure in order to refactor
        # code
        self.archives = dict()
        # Refer to define_archive_to_download() for the definition of the two
        # following attributes:
        self.archive_to_download = None
        self.archive_keyname = None

        # Although the archive is spelled out the BATI string (which
        # stands for "constructed" in french) is holds a BATI cityGML
        # where BATI is here understood as building
        pattern = parameters.pattern
        if (
            pattern == "BATI"
            or pattern == "TIN"
            or pattern == "WATER"
            or pattern == "PONT"
        ):
            self.pattern = pattern
        else:
            logging.info(f"Unknown pattern {pattern}. Exiting")
            sys.exit(1)

    def create_output_dir(self):
        if not os.path.isdir(self.results_dir):
            os.makedirs(self.results_dir)

    def define_archive_to_download(self):
        repository = "https://download.data.grandlyon.com/files/grandlyon/" "imagerie/"
        url = (
            repository
            + str(self.vintage)
            + "/maquette/"
            + self.borough
            + "_"
            + str(self.vintage)
            + ".zip"
        )
        self.key_name = self.borough + "_" + str(self.vintage)
        filename = os.path.join(
            self.key_name,
            self.get_vintage_borough_output_file_basename(self.vintage, self.borough),
        )
        self.archive_to_download = CityGMLFileFromArchive(
            url=url, name=filename, year=self.vintage
        )
        self.archives[self.key_name] = self.archive_to_download

    def register_archives_to_sanitize(self):
        """Sanitizing files is the exception"""
        # Vintage 2009
        if "LYON_4EME_2009" in self.archives:
            self.archives["LYON_4EME_2009"]["old_name"] = "LYON_4_BATI_2009.gml"
        if "LYON_5EME_2009" in self.archives:
            self.archives["LYON_5EME_2009"]["old_name"] = "LYON_5_BATI_2009.gml"
        if "LYON_7EME_2009" in self.archives:
            self.archives["LYON_7EME_2009"]["patch_filename"] = os.path.join(
                LyonMetropoleDowloadAndSanitize.patches_directory,
                "LYON_7EME_BATI_2009.gml.patch",
            )
        if "LYON_8EME_2009" in self.archives:
            self.archives["LYON_8EME_2009"]["patch_filename"] = os.path.join(
                LyonMetropoleDowloadAndSanitize.patches_directory,
                "LYON_8EME_BATI_2009.gml.patch",
            )
        # Vintage 2012
        if "LYON_7EME_2012" in self.archives:
            self.archives["LYON_7EME_2012"]["patch_filename"] = os.path.join(
                LyonMetropoleDowloadAndSanitize.patches_directory,
                "LYON_7EME_BATI_2012.gml.patch",
            )
        if "LYON_8EME_2012" in self.archives:
            self.archives["LYON_8EME_2012"]["patch_filename"] = os.path.join(
                LyonMetropoleDowloadAndSanitize.patches_directory,
                "LYON_8EME_BATI_2012.gml.patch",
            )

        # Vintage 2015
        if "LYON_7EME_2015" in self.archives:
            self.archives["LYON_7EME_2015"]["old_name"] = "LYON_7_BATI_2015.gml"

    def run(self):
        self.create_output_dir()
        self.define_archive_to_download()
        self.register_archives_to_sanitize()
        archive = self.archive_to_download
        # Specify the target directory
        archive.set_output_directory(self.results_dir)
        archive.set_tidy_up()  # Comment out for debugging
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
        archive.set_output_directory(os.path.join(self.results_dir, self.key_name))
        archive.set_filename(os.path.basename(archive.get_filename()))
        archive.rename_when_needed()
        archive.patch_when_needed()
        archive.assert_file_exists()

    def get_vintage_borough_output_file_basename(self, vintage, borough):
        return borough + "_" + self.pattern + "_" + str(vintage) + ".gml"

    def get_resulting_filenames(self):
        result = list()
        for dummy, archive in self.archives.items():
            archive.assert_file_exists()  # Just making sure
            result.append(archive.get_full_filename())
        return result

    def assert_output_files_exist(self):
        """
        :return: True when all the produced files do exist. False otherwise.
        """
        for filename in self.get_resulting_filenames():
            if not os.path.isfile(filename):
                logging.error(f"Output file {filename} not found.")
                return False
        return True
