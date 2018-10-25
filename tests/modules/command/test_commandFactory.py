from unittest import TestCase

from src.modules.command.command_factory import CommandFactory


class TestCommandFactory(TestCase):
    def test_get_command(self):
        c = CommandFactory.get_command('')
        self.assertEqual(len(c.arguments), 1)
        self.assertEqual(c.arguments[0], '')

        c = CommandFactory.get_command(' ')
        self.assertEqual(len(c.arguments), 1)
        self.assertEqual(c.arguments[0], '')

        c = CommandFactory.get_command('a ')
        self.assertEqual(len(c.arguments), 1)
        self.assertEqual(c.arguments[0], 'a')

        c = CommandFactory.get_command("żółć@ 'drugi argument'")
        self.assertEqual(len(c.arguments), 2)
        self.assertEqual(c.arguments[0], 'żółć@')
        self.assertEqual(c.arguments[1], 'drugi argument')

        c = CommandFactory.get_command("it's ''a' 'crazy' 'almost a good day' xD'' ")
        self.assertEqual(len(c.arguments), 5)
        self.assertEqual(c.arguments[0], "it's")
        self.assertEqual(c.arguments[1], "'a")
        self.assertEqual(c.arguments[2], 'crazy')
        self.assertEqual(c.arguments[3], 'almost a good day')
        self.assertEqual(c.arguments[4], "xD''")
