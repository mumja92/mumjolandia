import logging
import shutil
import os
from src.utils.shared_preferences import SharedPreferences
from unittest import TestCase
# todo: what with None and empty values?

class TestSharedPreferences(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSharedPreferences, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True
        self.preferences_location = 'data/preferences.pickle'

    def setUp(self):
        os.mkdir('data')

    def tearDown(self):
        shutil.rmtree(os.path.abspath(os.curdir) + '/data')

    def test_save_and_load(self):
        s = SharedPreferences(self.preferences_location)
        self.assertEqual(s.get('important_data'), None)
        self.assertEqual(s.get('different_important_data'), None)
        s.put('important_data', 'secret_value')
        s.put('different_data', 'different_secret_value')
        self.assertEqual(s.get('important_data'), 'secret_value')
        self.assertEqual(s.get('different_data'), 'different_secret_value')

    def test_overwrite_data(self):
        s = SharedPreferences(self.preferences_location)
        self.assertEqual(s.get('important_data'), None)
        s.put('important_data', 'secret_value')
        s.put('important_data', 'different_value')
        self.assertEqual(s.get('important_data'), 'different_value')

    def test_other_instance(self):
        s1 = SharedPreferences(self.preferences_location)
        self.assertEqual(s1.get('important_data'), None)
        s1.put('important_data', 'secret_value')
        s2 = SharedPreferences(self.preferences_location)
        self.assertEqual(s2.get('important_data'), 'secret_value')

    def test_load_non_existing_data(self):
        s = SharedPreferences(self.preferences_location)
        self.assertEqual(s.get('non_existing_data'), None)

    def test_clear_with_starting_pattern(self):
        start_string = 'find_me'
        non_start_string_first = 'ind_me'
        non_start_string_second = 'find_m'

        key1 = start_string + 'some_data'
        key2 = start_string + '_different_data'
        key3 = non_start_string_first + '_some_data'
        key4 = non_start_string_second + 'some_data'

        data1 = 'some_data1'
        data2 = 'some_data2'
        data3 = 'some_data3'
        data4 = 'some_data4'

        s = SharedPreferences(self.preferences_location)
        s.put(key1, data1)
        s.put(key2, data2)
        s.put(key3, data3)
        s.put(key4, data4)

        self.assertEqual(s.get(key1), data1)
        self.assertEqual(s.get(key2), data2)
        self.assertEqual(s.get(key3), data3)
        self.assertEqual(s.get(key4), data4)

        s.clear_starting_pattern(start_string)

        self.assertEqual(s.get(key1), None)
        self.assertEqual(s.get(key2), None)
        self.assertEqual(s.get(key3), data3)
        self.assertEqual(s.get(key4), data4)

    def test_clear_key(self):
        key1 = 'delete_me'
        key2 = 'delete_me_not'

        data1 = 'some_data1'
        data2 = 'some_data2'

        s = SharedPreferences(self.preferences_location)
        s.put(key1, data1)
        s.put(key2, data2)

        self.assertEqual(s.get(key1), data1)
        self.assertEqual(s.get(key2), data2)

        s.clear_key(key1)

        self.assertEqual(s.get(key1), None)
        self.assertEqual(s.get(key2), data2)
