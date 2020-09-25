# Simplified example code for running xml2_wiki

from shutil import move
from hed.utilities import tag_format
from hed.schema import constants

if __name__ == '__main__':
    result_dict = tag_format.check_for_duplicate_tags("HED7.1.1.xml")
    output_location = result_dict[constants.HED_OUTPUT_LOCATION_KEY]
    move(output_location, "results.txt")