import logging
import shutil
import os
from src.utils.shared_preferences import SharedPreferences
from unittest import TestCase


class TestSharedPreferences(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestSharedPreferences, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def setUp(self):
        os.mkdir('data')

    def tearDown(self):
        shutil.rmtree(os.path.abspath(os.curdir) + '/data')

    def test_save_and_load(self):
        s = SharedPreferences('data/preferences.pickle')
        self.assertEqual(s.get('important_data'), None)
        self.assertEqual(s.get('different_important_data'), None)
        s.put('important_data', 'secret_value')
        s.put('different_data', 'different_secret_value')
        self.assertEqual(s.get('important_data'), 'secret_value')
        self.assertEqual(s.get('different_data'), 'different_secret_value')

    def test_overwrite_data(self):
        s = SharedPreferences('data/preferences.pickle')
        self.assertEqual(s.get('important_data'), None)
        s.put('important_data', 'secret_value')
        s.put('important_data', 'different_value')
        self.assertEqual(s.get('important_data'), 'different_value')

    def test_other_instance(self):
        s1 = SharedPreferences('data/preferences.pickle')
        self.assertEqual(s1.get('important_data'), None)
        s1.put('important_data', 'secret_value')
        s2 = SharedPreferences('data/preferences.pickle')
        self.assertEqual(s2.get('important_data'), 'secret_value')

    def test_load_non_existing_data(self):
        s = SharedPreferences('data/preferences.pickle')
        s.put('important_data', 'secret_value')
        self.assertEqual(s.get('non_existing_data'), None)
