import unittest;
from validation import tag_validator, hed_dictionary;
import random;


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.hed_xml = '../tests/data/HED.xml';
        self.REQUIRE_CHILD_DICTIONARY_KEY = 'requireChild';
        self.hed_dictionary = hed_dictionary.populate_hed_dictionary(self.hed_xml);
        random_require_child_key = random.randint(0, len(self.hed_dictionary[self.REQUIRE_CHILD_DICTIONARY_KEY]));
        self.required_child_tag = \
            self.hed_dictionary[self.REQUIRE_CHILD_DICTIONARY_KEY][self.hed_dictionary[self.REQUIRE_CHILD_DICTIONARY_KEY].keys()[random_require_child_key]];
        self.invalid_original_tag = 'This/Is/A/Tag';
        self.invalid_formatted_tag = 'this/is/a/tag';
        self.valid_original_tag = 'Event/Label';
        self.valid_formatted_tag = 'event/label';
        self.tilde = '~';
        self.valid_is_numeric_tag = 'Attribute/Repetition/20';
        self.valid_unit_class_tag = 'Attribute/Temporal rate/20 Hz';
        self.valid_takes_value_tag = 'event/label/This is a label';
        self.valid_tag_group_string = 'This/Is/A/Tag ~ This/Is/Another/Tag ~ This/Is/A/Different/Tag';
        self.invalid_tag_group_string = 'This/Is/A/Tag ~ ~ This/Is/Another/Tag ~ This/Is/A/Different/Tag';
        self.valid_original_unique_tag_list = ['Event/Label/This is a label',
                                               'Event/Description/This is a description'];
        self.valid_formatted_unique_tag_list = ['event/label/this is a label',
             'event/description/this is a description'];
        self.invalid_original_unique_tag_list = ['Event/Label/This is a label', 'Event/Label/This is another label',
             'Event/Description/This is a description'];
        self.invalid_formatted_unique_tag_list = ['event/label/this is a label', 'event/label/this is another label',
             'event/description/this is a description'];
        self.valid_formatted_required_tag_list = ['event/label/this is a label', 'event/category/participant response',
             'event/description/this is a description'];
        self.invalid_formatted_required_tag_list = ['event/label/this is a label',
             'event/description/this is a description'];
        self.extension_allowed_descendant_tag = 'Item/Object/Tool/Hammer';

    def test_check_if_tag_is_valid(self):
        validation_error = tag_validator.check_if_tag_is_valid(self.hed_dictionary, self.invalid_original_tag, \
                                                               self.invalid_formatted_tag);
        self.assertIsInstance(validation_error, basestring);
        self.assertTrue(validation_error);
        validation_error = tag_validator.check_if_tag_is_valid(self.hed_dictionary, self.valid_original_tag, \
                                                               self.valid_formatted_tag);
        self.assertIsInstance(validation_error, basestring);
        self.assertFalse(validation_error);

    def test_check_if_tag_requires_child(self):
        validation_error = tag_validator.check_if_tag_requires_child(self.hed_dictionary, self.required_child_tag, \
                                                                     self.required_child_tag);
        self.assertIsInstance(validation_error, basestring);
        self.assertFalse(validation_error);

    def test_check_number_of_group_tildes(self):
        validation_error = tag_validator.check_number_of_group_tildes(self.valid_tag_group_string);
        self.assertIsInstance(validation_error, basestring);
        self.assertFalse(validation_error);
        validation_error = tag_validator.check_number_of_group_tildes(self.invalid_tag_group_string);
        self.assertIsInstance(validation_error, basestring);
        self.assertTrue(validation_error);

    def test_check_if_multiple_unique_tags_exist(self):
        validation_error = tag_validator.check_if_multiple_unique_tags_exist(self.hed_dictionary, \
                                                                             self.valid_original_unique_tag_list, \
                                                                             self.valid_formatted_unique_tag_list);
        self.assertIsInstance(validation_error, basestring);
        self.assertFalse(validation_error);
        validation_error = tag_validator.check_if_multiple_unique_tags_exist(self.hed_dictionary, \
                                                                             self.invalid_original_unique_tag_list, \
                                                                             self.invalid_formatted_unique_tag_list);
        self.assertIsInstance(validation_error, basestring);
        self.assertTrue(validation_error);

    def test_check_for_required_tags(self):
        validation_error = tag_validator.check_for_required_tags(self.hed_dictionary,
                                                                 self.valid_formatted_required_tag_list);
        self.assertIsInstance(validation_error, basestring);
        self.assertFalse(validation_error);
        validation_error = tag_validator.check_for_required_tags(self.hed_dictionary,
                                                                 self.invalid_formatted_required_tag_list);
        self.assertIsInstance(validation_error, basestring);
        self.assertTrue(validation_error);

    def test_get_tag_slash_indices(self):
        tag_slash_indices = tag_validator.get_tag_slash_indices(self.valid_formatted_tag);
        self.assertIsInstance(tag_slash_indices, list);

    def test_get_tag_substring_by_end_index(self):
        tag_slash_indices = tag_validator.get_tag_slash_indices(self.valid_formatted_tag);
        tag = tag_validator.get_tag_substring_by_end_index(self.valid_formatted_tag, tag_slash_indices[0]);
        self.assertIsInstance(tag, basestring);
        self.assertNotEqual(self.valid_formatted_tag, tag);
        tag = tag_validator.get_tag_substring_by_end_index(self.valid_formatted_tag, 0);
        self.assertEqual(self.valid_formatted_tag, tag);

    def test_is_extension_allowed_tag(self):
        extension_allowed_tag = tag_validator.is_extension_allowed_tag(self.hed_dictionary,
                                                                       self.extension_allowed_descendant_tag);
        self.assertTrue(extension_allowed_tag);
        extension_allowed_tag = tag_validator.is_extension_allowed_tag(self.hed_dictionary, self.valid_formatted_tag);
        self.assertFalse(extension_allowed_tag);

    def test_tag_takes_value(self):
        takes_value_tag = tag_validator.tag_takes_value(self.hed_dictionary, self.valid_takes_value_tag);
        self.assertTrue(takes_value_tag);
        takes_value_tag = tag_validator.tag_takes_value(self.hed_dictionary, self.valid_formatted_tag);
        self.assertFalse(takes_value_tag);

    def test_is_numeric_tag(self):
        numeric_tag = tag_validator.is_numeric_tag(self.hed_dictionary, self.valid_is_numeric_tag);
        self.assertTrue(numeric_tag);

    def test_is_unit_class_tag(self):
        unit_class_tag = tag_validator.is_unit_class_tag(self.hed_dictionary, self.valid_unit_class_tag);
        self.assertTrue(unit_class_tag);

if __name__ == '__main__':
    unittest.main();
