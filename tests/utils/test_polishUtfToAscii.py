from unittest import TestCase

from src.utils.polish_utf_to_ascii import PolishUtfToAscii


class TestPolishUtfToAscii(TestCase):
    def test_translate(self):
        string = 'qwęrtyuiópąśdfghjkłżźćvbńm'
        self.assertEqual('qwertyuiopasdfghjklzzcvbnm', PolishUtfToAscii.translate(string))
