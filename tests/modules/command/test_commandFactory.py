from unittest import TestCase
from src.modules.command.command_factory import CommandFactory


class TestCommandFactory(TestCase):
    def test_get_command(self):
        c = CommandFactory.get_command('żółć@')
        self.assertEquals(len(c.arguments), 1)
        self.assertEquals(c.arguments[0], 'żółć@')

        c = CommandFactory.get_command('xD xDD')
        self.assertEquals(len(c.arguments), 2)
        self.assertEquals(c.arguments[0], 'xD')
        self.assertEquals(c.arguments[1], 'xDD')

        c = CommandFactory.get_command('')
        self.assertEquals(len(c.arguments), 1)
        self.assertEquals(c.arguments[0], '')
