from unittest import TestCase

from src.modules.command.command_factory import CommandFactory


class TestCommandFactory(TestCase):
    def test_get_command(self):
        c = CommandFactory.get_command('')
        self.assertEquals(len(c.arguments), 1)
        self.assertEquals(c.arguments[0], '')

        c = CommandFactory.get_command(' ')
        self.assertEquals(len(c.arguments), 1)
        self.assertEquals(c.arguments[0], '')

        c = CommandFactory.get_command('a ')
        self.assertEquals(len(c.arguments), 1)
        self.assertEquals(c.arguments[0], 'a')

        c = CommandFactory.get_command("żółć@ 'drugi argument'")
        self.assertEquals(len(c.arguments), 2)
        self.assertEquals(c.arguments[0], 'żółć@')
        self.assertEquals(c.arguments[1], 'drugi argument')

        c = CommandFactory.get_command("it's ''a' 'crazy' 'almost a good day' xD'' ")
        self.assertEquals(len(c.arguments), 5)
        self.assertEquals(c.arguments[0], "it's")
        self.assertEquals(c.arguments[1], "'a")
        self.assertEquals(c.arguments[2], 'crazy')
        self.assertEquals(c.arguments[3], 'almost a good day')
        self.assertEquals(c.arguments[4], "xD''")
