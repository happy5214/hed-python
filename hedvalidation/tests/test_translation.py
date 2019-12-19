import random;
import unittest;
import os;

from hedvalidation.hed_string_delimiter import HedStringDelimiter;
from hedvalidation.hed_input_reader import HedInputReader;
from hedvalidation.error_reporter import report_error_type;
from hedvalidation.warning_reporter import report_warning_type;
from hedvalidation.tag_validator import TagValidator;
from hedvalidation.hed_dictionary import HedDictionary;

class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.generic_hed_input_reader = HedInputReader('Attribute/onset')
        hed_xml = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/HED.xml');
        hed_dictionary = HedDictionary(hed_xml);
        self.tagValidator = TagValidator(hed_dictionary)

    def validate(self, test_strings, expected_results, expected_issues):
        for test in test_strings:
            hed_tag_string = expected_results[test]
            target_result = expected_issues[test]

            validation_issues = self.generic_hed_input_reader._validate_hed_string(test_strings[test])

            has_no_issues = (validation_issues == "")
            matching_errors = validation_issues == target_result

            self.assertTrue(has_no_issues == hed_tag_string)

    def validate_syntactic_base(self, testStrings, expectedIssues, expectedResults, testFunction):
        for testKey in testStrings:
            parsedTestStrings = HedStringDelimiter(testStrings[testKey])
            testResult = testFunction(str(parsedTestStrings), str(testStrings[testKey]))
            expectedIssue = expectedIssues[testKey]
            expectedResult = expectedResults[testKey]
            has_no_issues = (testResult == "")
            self.assertEqual(testResult, expectedIssue, testStrings[testKey])
            self.assertCountEqual(testResult, expectedIssue, testStrings[testKey])

    def test_mismatched_parentheses(self):
        testStrings =   {
            'extraOpening': \
                '/Action/Reach/To touch,((/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px',
            'extraClosing': \
                '/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px',
            'valid': \
                '/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px'
        }
        expectedResults = {
            'extraOpening': False,
            'extraClosing': False,
            'valid': True
        }
        expectedIssues = {
            #I think this is right
            'extraOpening': report_error_type('bracket', tag=testStrings['extraOpening'].strip(), opening_bracket_count=2, closing_bracket_count=1),
            'extraClosing': report_error_type('bracket', tag=testStrings['extraClosing'].strip(), opening_bracket_count=1, closing_bracket_count=2),
            'valid': ''
        }

        self.validate(testStrings, expectedResults, expectedIssues)
##########################################################################################################################################
    # Validator does not properly report errors with commas and does not report any error for extra tildes. (issue 3)
###########################################################################################################################################
    # def test_malformed_delimiters(self):
    #     testStrings = {
    #         'missingOpeningComma' : \
    #             '/Action/Reach/To touch(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px',
    #         'missingCLosingComma' : \
    #             '/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm)/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px',
    #         'extraOpeningComma' : \
    #             ',/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px',
    #         'extraClosingComma' : \
    #             '/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px,',
    #         'extraOpeningTilde' : \
    #             '~/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px',
    #         'extraClosingTilde' : \
    #             '/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px~',
    #         'multipleExtraOpeningDelimiters' : \
    #             ',~,/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px',
    #         'multipleExtraClosingDelimiters' : \
    #             '/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px,~~,',
    #         'multipleExtraMiddleDelimiters' : \
    #             '/Action/Reach/To touch,,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,~,/Attribute/Location/Screen/Left/23 px',
    #         'valid' : \
    #             '/Action/Reach/To touch,(/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px',
    #         'validNestedParentheses' : \
    #             '/Action/Reach/To touch,((/Attribute/Object side/Left,/Participant/Effect/Body part/Arm),/Attribute/Location/Screen/Top/70 px,/Attribute/Location/Screen/Left/23 px),Event/Duration/3 ms',
    #     }
    #
    #     expectedResults = {
    #         'missingOpeningComma' : False,
    #         'missingClosingComma' : False,
    #         'extraOpeningComma' : False,
    #         'extraClosingComma' : False,
    #         'extraOpeningTilde' : False,
    #         'extraClosingTilde' : False,
    #         'multipleExtraOpeningDelimiters' : False,
    #         'multipleExtraClosingDelimiters' : False,
    #         'multipleExtraMiddleDelimiters' : False,
    #         'valid' : True,
    #         'validNestedParentheses' : True
    #     }
    #     expectedIssues = {
    #         #NOT COMPLETE
    #         'missingOpeningComma' : report_error_type('comma'),
    #         'missingClosingComma': report_error_type('comma'),
    #         'extraOpeningComma': report_error_type('comma'),
    #         'extraClosingComma': report_error_type('comma'),
    #         'extraOpeningTilde': report_error_type('tilde'),
    #         'extraClosingTilde': report_error_type('tilde'),
    #         'multipleExtraOpeningDelimiters': report_error_type('comma'),
    #         'multipleExtraClosingDelimiters': report_error_type('comma'),
    #         'multipleExtraMiddleDelimiters': report_error_type('comma'),
    #         'valid': '',
    #         'validNestedParentheses': ''
    #     }
    #
    #     self.validate(testStrings, expectedResults, expectedIssues)

    def test_invalid_characters(self):
        testStrings = {
            'openingBrace' : \
                '/Attribute/Object side/Left,/Participant/Effect{/Body part/Arm',
            'closingBrace' : \
                '/Attribute/Object side/Left,/Participant/Effect}/Body part/Arm',
            'openingBracket' : \
                '/Attribute/Object side/Left,/Participant/Effect[/Body part/Arm',
            'closingBracket' : \
                '/Attribute/Object side/Left,/Participant/Effect]/Body part/Arm'
        }
        expectedResults = {
            'openingBrace' : False,
            'closingBrace' : False,
            'openingBracket' : False,
            'closingBracket' : False
        }
        expectedIssues = {
            #NOT COMPLETE
            'openingBrace' : report_error_type('character', tag='{'),
            'closingBrace' : report_error_type('character', tag='}'),
            'openingBracket' : report_error_type('character', tag='['),
            'closingBracket' : report_error_type('character', tag=']')
        }
        self.validate(testStrings, expectedResults, expectedIssues)

    def test_exist_in_schema(self):
        testString = {
            'takesValue' : 'Event/Duration/3 ms',
            'full' : 'Attribute/Object side/Left',
            'extensionsAllowed' : 'Item/Object/Person/Driver',
            'leafExtension' : 'Action/Hum/Song',
            'nonExtensionsAllowed' : 'Item/Nonsense',
            'illegalComma' : 'Event/Label/This is a label,This/Is/A/Tag'
        }
        expectedResults = {
            'takesValue': True,
            'full': True,
            'extensionsAllowed': True,
            'leafExtension': False,
            'nonExtensionsAllowed': False,
            'illegalComma': False
        }
        expectedIssues = {
            'takesValue': '',
            'full': '',
            'extensionsAllowed': '',
            'leafExtension': report_error_type('valid', tag=testString['leafExtension']),
            'nonExtensionsAllowed': report_error_type('valid', tag=testString['nonExtensionsAllowed']),
            'illegalComma': report_error_type('comma', previous_tag='Event/Label/This is a label', tag='This/Is/A/Tag')
        }
        #alex used semantic validation
        self.validate(testString,expectedResults,expectedIssues)

    def validate_syntactic(self,testStrings, expectedResults, expectedIssues, checkForWarnings):
        self.validate_syntactic_base(testStrings,expectedResults,expectedIssues, lambda parsedString, originalTag:
        self.tagValidator.check_capitalization(formatted_tag=parsedString, original_tag=originalTag))

    def test_proper_capitalization(self):
        # errors with camelCase test string not being a valid test string
        testString = {
            'proper' : 'Event/Category/Experimental stimulus',
            'camelCase' : 'DoubleEvent/Something',
            'takesValue' : 'Attribute/Temporal rate/20 Hz',
            'numeric' : 'Attribute/Repetition/20',
            'lowercase' : 'Event/something'
        }
        expectedResults = {
            'proper': True,
            'camelCase': True,
            'takesValue': True,
            'numeric': True,
            'lowercase': False
        }
        expectedIssues = {
            #NOT COMPLETE
            'proper': '',
            'camelCase': '',
            'takesValue': '',
            'numeric': '',
            'lowercase': report_warning_type('cap', tag=testString['lowercase'])
        }
        # needs to use semantic valdiation
        self.validate_syntactic(testStrings=testString, expectedIssues=expectedResults, expectedResults=expectedIssues, checkForWarnings=True)
#######################################################################################################
    # # need to address issue 3 before this test will preform properly
#######################################################################################################
    # def test_no_more_than_two_tildes(self):
    #     testStrings = {
    #         'noTildeGroup': 'Event/Category/Experimental stimulus,(Item/Object/Vehicle/Train,Event/Category/Experimental stimulus)',
    #         'oneTildeGroup': 'Event/Category/Experimental stimulus,(Item/Object/Vehicle/Car ~ Attribute/Object control/Perturb)',
    #         'twoTildeGroup': 'Event/Category/Experimental stimulus,(Participant/ID 1 ~ Participant/Effect/Visual ~ Item/Object/Vehicle/Car, Item/ID/RedCar, Attribute/Visual/Color/Red)',
    #         'invalidTildeGroup': 'Event/Category/Experimental stimulus,(Participant/ID 1 ~ Participant/Effect/Visual ~ Item/Object/Vehicle/Car, Item/ID/RedCar, Attribute/Visual/Color/Red ~ Attribute/Object control/Perturb)',
    #     }
    #     expectedResults = {
    #         'noTildeGroup': True,
    #         'oneTildeGroup': True,
    #         'twoTildeGroup': True,
    #         'invalidTildeGroup': False
    #     }
    #     expectedIssues = {
    #         'noTildeGroup': '',
    #         'oneTildeGroup': '',
    #         'twoTildeGroup': '',
    #         'invalidTildeGroup': report_error_type('tilde', tag='Event/Category/Experimental stimulus,(Participant/ID 1 ~ Participant/Effect/Visual ~ Item/Object/Vehicle/Car, Item/ID/RedCar, Attribute/Visual/Color/Red ~ Attribute/Object control/Perturb)')
    #     }
    #     # uses seemantic validaiton
    #     self.validate(testStrings, expectedResults, expectedIssues)
########################################################################
    # inside of the error reporter there is nothing to deal with required prefix missing
########################################################################
    # def validate_syntactic_1(self,testStrings, expectedResults, expectedIssues):
    #     self.validate_syntactic_base(testStrings, expectedResults, expectedIssues, lambda parsedString, originalTag:
    #    self.tagValidator.run_top_level_validators(formatted_top_level_tags=parsedString))
    #
    # # requires semantic validator
    # def test_includes_all_required_tags(self):
    #     testStrings = {
    #         'complete': 'Event/Label/Bus,Event/Category/Experimental stimulus,Event/Description/Shown a picture of a bus,Item/Object/Vehicle/Bus',
    #         'missingLabel': 'Event/Category/Experimental stimulus,Event/Description/Shown a picture of a bus,Item/Object/Vehicle/Bus',
    #         'missingCategory': 'Event/Label/Bus,Event/Description/Shown a picture of a bus,Item/Object/Vehicle/Bus',
    #         'missingDescription': 'Event/Label/Bus,Event/Category/Experimental stimulus,Item/Object/Vehicle/Bus',
    #         'missingAllRequired': 'Item/Object/Vehicle/Bus',
    #     }
    #     expectedResults = {
    #         'complete': True,
    #         'missingLabel': False,
    #         'missingCategory': False,
    #         'missingDescription': False,
    #         'missingAllRequired': False,
    #     }
    #     expectedIssues = {
    #         'complete': "",
    #         'missingLabel': "report_error_type()",
    #         'missingCategory': "report_error_type()",
    #         'missingDescription': "report_error_type()",
    #         'missingAllRequired': "report_error_type()",
    #     }
    #     # uses semnatic validator
    #     self.validate_syntactic_1(testStrings, expectedResults, expectedIssues)

    def child_required(self):
        testString = {
            'hasChild' : 'Event/Category/Experimental stimulus',
            'missingChild' : 'Event/Category'
        }
        expectedResults = {
            'hasChild' : True,
            'missingChild' : False
        }
        expectedIssues = {
            #NOT COMPLETE
            'hasChild' : [],
            'missingChild' : [error_reporter.report_error_type()]
        }
        validator(testString,expectedResults, expectedIssues)
    #
    # def required_units(self):
    #     testString = {
    #         'hasRequiredUnit' : 'Event/Duration/3 ms',
    #         'missingRequiredUnit' : 'Event/Duration/3',
    #         'notRequiredNumber' : 'Attribute/Color/Red/0.5',
    #         'notRequiredScientific' : 'Attribute/Color/Red/5.2e-1',
    #         'timeValue' : 'Item/2D shape/Clock face/8:30'
    #     }
    #     expectedResults = {
    #         'hasRequiredUnit': True,
    #         'missingRequiredUnit': False,
    #         'notRequiredNumber': True,
    #         'notRequiredScientific': True,
    #         'timeValue': True
    #     }
    #     expectedIssues = {
    #         #NOT COMPLETE
    #         'hasRequiredUnit': [],
    #         'missingRequiredUnit': [error_reporter.report_error_type()],
    #         'notRequiredNumber': [],
    #         'notRequiredScientific': [],
    #         'timeValue': []
    #     }
    #     validator(testString, expectedResults, expectedIssues)
    #
    # def correct_units(self):
    #     testString = {
    #         'correctUnit' : 'Event/Duration/3 ms',
    #         'correctUnitScientific' : 'Event/Duration/3.5e1 ms',
    #         'incorrectUnit' : 'Event/Duration/3 cm',
    #         'notRequiredNumber' : 'Attribute/Color/Red/0.5',
    #         'notRequiredScientific' : 'Attribute/Color/Red/5e-1',
    #         'properTime' : 'Item/2D shape/Clock face/8:30',
    #         'invalidTime' : 'Item/2D shape/Clock face/54:54'
    #     }
    #     expectedResults = {
    #         'correctUnit': True,
    #         'correctUnitScientific': True,
    #         'incorrectUnit': False,
    #         'notRequiredNumber': True,
    #         'notRequiredScientific': True,
    #         'properTime': True,
    #         'invalidTime': False
    #     }
    #     legalTimeUnits = [
    #         's',
    #         'second',
    #         'seconds',
    #         'centiseconds',
    #         'centisecond',
    #         'cs',
    #         'hour:min',
    #         'day',
    #         'days',
    #         'ms',
    #         'milliseconds',
    #         'millisecond',
    #         'minute',
    #         'minutes',
    #         'hour',
    #         'hours',
    #         ]
    #     expectedIssues = {
    #         #NOT COMPLETE
    #         'correctUnit': [],
    #         'correctUnitScientific': [],
    #         'incorrectUnit': [error_reporter.report_error_type()],
    #         'notRequiredNumber': [],
    #         'notRequiredScientific': [],
    #         'properTime': [],
    #         'invalidTime': [error_reporter.report_error_type()]
    #     }
    #     validator(testString, expectedResults, expectedIssues)
    # def test_no_duplicates(self):
    #         testStrings = {
    #             'topLevelDuplicate': 'Event/Category/Experimental stimulus,Event/Category/Experimental stimulus',
    #             'groupDuplicate': 'Item/Object/Vehicle/Train,(Event/Category/Experimental stimulus,Attribute/Visual/Color/Purple,Event/Category/Experimental stimulus)',
    #             'noDuplicate': 'Event/Category/Experimental stimulus,Item/Object/Vehicle/Train,Attribute/Visual/Color/Purple',
    #             'legalDuplicate':'Item/Object/Vehicle/Train,(Item/Object/Vehicle/Train,Event/Category/Experimental stimulus)',
    #         }
    #         expectedResults = {
    #             'topLevelDuplicate': False,
    #             'groupDuplicate': False,
    #             'legalDuplicate': True,
    #             'noDuplicate': True
    #         }
    #         expectedIssues = {
    #             'topLevelDuplicate':  report_error_type(),
    #             'groupDuplicate': report_error_type(),
    #             'legalDuplicate': report_error_type(),
    #             'noDuplicate': True
    #         }
            # alex used semantic validation here
    #        validator(testStrings, expectedResults, expectedIssues)
    # def multiple_copies_unique_tags(self):
    #     testStrings = {
    #         'legal': 'Event/Description/Rail vehicles,Item/Object/Vehicle/Train,(Item/Object/Vehicle/Train,Event/Category/Experimental stimulus)',
    #         'multipleDesc': 'Event/Description/Rail vehicles,Event/Description/Locomotive-pulled or multiple units,Item/Object/Vehicle/Train,(Item/Object/Vehicle/Train,Event/Category/Experimental stimulus)'
    #     }
    #     expectedResults = {
    #         'legal': True,
    #         'multipleDesc': False
    #     }
    #     expectedIssues = {
    #         'legal': report_error_type(),
    #         'multipleDesc': report_error_type()
    #     }
    #     # alex used seantic validation here
    #     validator(testStrings, expectedResults, expectedIssues)
