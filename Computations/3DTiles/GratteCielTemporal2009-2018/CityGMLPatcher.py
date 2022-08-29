import argparse
import logging
from unittest.mock import patch
from lxml import etree

def main():
    """
    It takes a CityGML file, a CityDoctor2 error file, and an output file, and it removes all the
    invalid features from the CityGML file
    """
    parser = argparse.ArgumentParser(description='Remove invalid CityGML 2.0 building features using a CityDoctor2 validation output. For documentation on how to install and use CityDoctor2, see https://transfer.hft-stuttgart.de/gitlab/citydoctor/citydoctor2')
    parser.add_argument('input_file', help='Specify the input file')
    parser.add_argument('error_file', help='Specify the error file output from CityDoctor')
    parser.add_argument('output_file', help='Specify the output file')
    parser.add_argument('-i', '--ignore_errors', default='', help='Specify a comma separated list of errors to ignore during patching')
    parser.add_argument('-l', '--log', default='output.log', help='Specify logfile')
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        filename=args.log,
                        level=logging.WARNING)

    logging.info(f'patching input file: {args.input_file}...')
    patcher = GMLPatcher(args.input_file, args.error_file, args.output_file, args.ignore_errors)
    patcher.patch()
    logging.info('done')


# It removes all buildings from the input xml that have errors in the error xml
class GMLPatcher():
    def __init__(self, input_file, error_file, output_file, ignore_list):
        """
        A constructor function. It takes in the input file, error file, output file, and ignore list. It
        then parses the input file, error file, and output file.
        
        :param input_file: The file that contains the XML that you want to modify
        :param error_file: The a CityDoctor output file that contains the errors
        :param output_file: The file that will be written to
        :param ignore_list: A list of strings that are the names of the elements that you want to ignore
        """
        parser = etree.XMLParser(remove_comments=True)
        self.input_file = input_file
        self.error_file = error_file
        self.output_file = output_file
        self.ignore_list = str(ignore_list).split(',')
        self.input_xml = etree.parse(input_file, parser)
        self.error_xml = etree.parse(error_file, parser)
        self.output_xml = etree.parse(input_file, parser)

    def patch(self):
        """
        It removes all buildings from the input xml that have errors in the error xml
        """
        cd = r'{http://www.citydoctor.eu}'                          # citydoctor namespace
        gml = r'{http://www.opengis.net/gml}'
        bldg = r'{http://www.opengis.net/citygml/building/2.0}'     # citygml building namespace
        patch_count = 0
        # logging.info('error count:')
        # for error in self.error_xml.findall(f'.//{cd}global_statistics/{cd}errors/{cd}error'):
        #     logging.info(f'  {error.attrib["name"]} {error.text}')
        for building in self.error_xml.getroot().findall(f'.//{cd}validation_results/{cd}building_report'):
            tag = building.attrib["gml_id"]
            error_list = [error.attrib['name'] for error
                in building.findall(f'.//{cd}error_statistics/{cd}error')
                if error.attrib['name'] not in self.ignore_list]
            if len(error_list) > 0:
                logging.info(f'found error(s): {error_list} in {tag}')
                output_building = self.output_xml.find(f'.//{bldg}Building[@{gml}id=\"{tag}\"]')
                if output_building is None:
                    logging.warning(f'building {tag} not found in input file')
                output_building.getparent().getparent().remove(output_building.getparent())
                patch_count += 1
        logging.info(f'removed {patch_count} building(s), writing output to file...')
        # write patched xml to output
        with open(self.output_file, 'wb') as file:
            file.write(etree.tostring(self.output_xml, pretty_print=True, xml_declaration=True))

            
if __name__ == "__main__":
    main()


# Tests
# python CityGMLPatcher.py --ignore_errors SE_ATTRIBUTE_MISSING ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2009/VILLEURBANNE_BATI_2009.gml ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2009/output2009.xml ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2009/VILLEURBANNE_BATI_2009_patched.gml
# python CityGMLPatcher.py --ignore_errors SE_ATTRIBUTE_MISSING ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2012/VILLEURBANNE_BATI_2012.gml ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2012/output2012.xml ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2012/VILLEURBANNE_BATI_2012_patched.gml
# python CityGMLPatcher.py --ignore_errors SE_ATTRIBUTE_MISSING,GE_P_NON_PLANAR_POLYGON_DISTANCE_PLANE,GE_S_MULTIPLE_CONNECTED_COMPONENTS ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2015/VILLEURBANNE_BATI_2015.gml ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2015/output2015.xml ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2015/VILLEURBANNE_BATI_2015_patched.gml
# python CityGMLPatcher.py --ignore_errors SE_ATTRIBUTE_MISSING,GE_P_NON_PLANAR_POLYGON_DISTANCE_PLANE,GE_S_MULTIPLE_CONNECTED_COMPONENTS ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2018/VILLEURBANNE_BATI_2018.gml ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2018/output2018.xml ../../../../../../Desktop/Datasets/GratteCiel_2009-2018v2/VILLEURBANNE_2018/VILLEURBANNE_BATI_2018_patched.gml