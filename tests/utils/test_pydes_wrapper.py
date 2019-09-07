from unittest import TestCase

import logging

from src.utils.pydes_wrapper import PydesWrapper


class TestPydesWrapper(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPydesWrapper, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def setUp(self):
        self.pw = PydesWrapper()
        pass

    def test_encrypt_ok(self):
        password = 'wieloryby234'
        sensitive_data = 'Important data. Please take care!'
        a = self.pw.encrypt(password, sensitive_data)
        b = self.pw.decrypt(password, a)
        self.assertTrue(isinstance(a, str))
        self.assertTrue(isinstance(b, str))
        self.assertNotEqual(sensitive_data, a)
        self.assertEqual(sensitive_data, b)

    def test_encrypt_nook(self):
        password = 'wieloryby234'
        wrong_password = 'different_password'
        sensitive_data = 'Important data. Please take care!'
        a = self.pw.encrypt(password, sensitive_data)
        b = self.pw.decrypt(wrong_password, a)
        self.assertTrue(isinstance(a, str))
        self.assertTrue(isinstance(b, str))
        self.assertNotEqual(sensitive_data, a)
        self.assertNotEqual(sensitive_data, b)

    def test_empty_password_nook(self):
        password = None
        sensitive_data = 'Important data. Please take care!'
        a = self.pw.encrypt(password, sensitive_data)
        self.assertTrue(a is None)

        password = ''
        a = self.pw.encrypt(password, sensitive_data)
        self.assertTrue(a is None)

    def test_empty_data_nook(self):
        password = 'wieloryby234'
        sensitive_data = None
        a = self.pw.encrypt(password, sensitive_data)
        self.assertTrue(a is None)

        sensitive_data = ''
        a = self.pw.encrypt(password, sensitive_data)
        self.assertTrue(a is None)

    def test_data_non_ascii_characters(self):
        password = 'wieloryby234'
        sensitive_data = 'ąśćźżó'
        a = self.pw.encrypt(password, sensitive_data)
        b = self.pw.decrypt(password, a)
        self.assertTrue(a is None)
        self.assertTrue(b is None)
        self.assertNotEqual(sensitive_data, b)

    def test_password_non_ascii_characters(self):
        password = 'mąka'
        sensitive_data = 'Important data. Please take care!'
        a = self.pw.encrypt(password, sensitive_data)
        b = self.pw.decrypt(password, a)
        self.assertTrue(a is None)
        self.assertTrue(b is None)
        self.assertNotEqual(sensitive_data, b)

    def test_password_too_short(self):
        password = 'short'
        sensitive_data = 'Important data. Please take care!'
        a = self.pw.encrypt(password, sensitive_data)
        b = self.pw.decrypt(password, a)
        self.assertTrue(a is None)
        self.assertTrue(b is None)
        self.assertNotEqual(sensitive_data, b)