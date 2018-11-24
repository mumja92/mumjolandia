from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.interface.mumjolandia.mumjolandia_cli_mode import MumjolandiaCliMode
from src.interface.mumjolandia.mumjolandia_immutable_type_wrapper import MumjolandiaImmutableTypeWrapper
from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.mumjolandia_data_passer import MumjolandiaDataPasser
from src.modules.mumjolandia.cli.mumjolandia_cli import MumjolandiaCli
from src.modules.mumjolandia.cli.mumjolandia_cli_printer import MumjolandiaCliPrinter
from src.utils.hidden_prints import HiddenPrints


class TestMumjolandiaCli(TestCase):
    def setUp(self):
        self.dp = MumjolandiaDataPasser(1, 1, 1, 1)
        self.cli = MumjolandiaCli(self.dp)
        self.cp = MumjolandiaCliPrinter(1)

        # cli.run() exits when flag is raised, but for some commands (mode, cls) the check is skipped.
        # to exit, it is necessary to call extra command that is passed to DataPasser (so the flag check will occur)
        def execute_patched():
            self.cli.exit_flag = MumjolandiaImmutableTypeWrapper(True)
            return None

        self.cp.execute = MagicMock(side_effect=execute_patched())
        self.cli.cli_printer = self.cp

    @patch('src.modules.mumjolandia.mumjolandia_data_passer.MumjolandiaDataPasser.pass_command', return_value=None)
    @patch('src.modules.console.console.Console.get_next_command',
           side_effect=[CommandFactory.get_command('mode'),
                        CommandFactory.get_command('test'),
                        CommandFactory.get_command('mode task'),
                        CommandFactory.get_command('test'),
                        CommandFactory.get_command('mode food'),
                        CommandFactory.get_command('test'),
                        CommandFactory.get_command('mode invalid'),
                        CommandFactory.get_command('test'),
                        CommandFactory.get_command('mode none'),
                        CommandFactory.get_command('test'),
                        CommandFactory.get_command('mode game'),
                        CommandFactory.get_command('test'),
                        CommandFactory.get_command('mode'),
                        CommandFactory.get_command('test')])
    def test_change_modes(self, mock_command, mock_passer):
        with HiddenPrints():
            self.cli.run()
            self.assertEqual(self.cli.mode, MumjolandiaCliMode.none)
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('test'))
            self.assertEqual(mock_command.call_count, 2)
            self.assertEqual(mock_passer.call_count, 1)

            self.cli.run()
            self.assertEqual(self.cli.mode, MumjolandiaCliMode.task)
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('task test'))
            self.assertEqual(mock_command.call_count, 4)
            self.assertEqual(mock_passer.call_count, 2)

            self.cli.run()
            self.assertEqual(self.cli.mode, MumjolandiaCliMode.food)
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('food test'))
            self.assertEqual(mock_command.call_count, 6)
            self.assertEqual(mock_passer.call_count, 3)

            self.cli.run()
            self.assertEqual(self.cli.mode, MumjolandiaCliMode.food)
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('food test'))
            self.assertEqual(mock_command.call_count, 8)
            self.assertEqual(mock_passer.call_count, 4)

            self.cli.run()
            self.assertEqual(self.cli.mode, MumjolandiaCliMode.none)
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('test'))
            self.assertEqual(mock_command.call_count, 10)
            self.assertEqual(mock_passer.call_count, 5)

            self.cli.run()
            self.assertEqual(self.cli.mode, MumjolandiaCliMode.game)
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('game test'))
            self.assertEqual(mock_command.call_count, 12)
            self.assertEqual(mock_passer.call_count, 6)

            self.cli.run()
            self.assertEqual(self.cli.mode, MumjolandiaCliMode.none)
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('test'))
            self.assertEqual(mock_command.call_count, 14)
            self.assertEqual(mock_passer.call_count, 7)

    @patch('src.modules.mumjolandia.cli.mumjolandia_cli.MumjolandiaCli._MumjolandiaCli__clear_screen', return_value=None)
    @patch('src.modules.mumjolandia.mumjolandia_data_passer.MumjolandiaDataPasser.pass_command', return_value=None)
    @patch('src.modules.console.console.Console.get_next_command',
           side_effect=[CommandFactory.get_command('cls'),
                        CommandFactory.get_command('needed_to_exit_loop'),
                        CommandFactory.get_command('path'),
                        CommandFactory.get_command('needed_to_exit_loop')])
    def test_not_passable_commands(self, mock_command, mock_passer, mock_cls):
        with HiddenPrints():
            self.cli.run()
            self.assertEqual(mock_command.call_count, 2)
            self.assertEqual(mock_passer.call_count, 1)
            self.assertEqual(mock_cls.call_count, 1)

            self.cli.run()
            self.assertEqual(mock_command.call_count, 4)
            self.assertEqual(mock_passer.call_count, 2)
            self.assertEqual(mock_cls.call_count, 1)

    @patch('src.modules.mumjolandia.mumjolandia_data_passer.MumjolandiaDataPasser.pass_command', return_value=None)
    @patch('src.modules.console.console.Console.get_next_command',
           side_effect=[CommandFactory.get_command('task print')])
    def test_task_print(self, mock_command, mock_passer):
        with HiddenPrints():
            self.cli.run()
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('task get'))
            self.assertEqual(mock_command.call_count, 1)
            self.assertEqual(mock_passer.call_count, 1)

    @patch('src.modules.mumjolandia.mumjolandia_data_passer.MumjolandiaDataPasser.pass_command', return_value=None)
    @patch('src.modules.console.console.Console.get_next_command',
           side_effect=[CommandFactory.get_command('task edit 1 name'),
                        CommandFactory.get_command('task edit name name'),
                        CommandFactory.get_command('needed_to_exit_loop'),
                        CommandFactory.get_command('task edit name'),
                        CommandFactory.get_command('needed_to_exit_loop'),
                        CommandFactory.get_command('task edit 1'),
                        CommandFactory.get_command('needed_to_exit_loop'),
                        CommandFactory.get_command('task edit'),
                        CommandFactory.get_command('needed_to_exit_loop')])
    def test_task_edit(self, mock_command, mock_passer):
        with HiddenPrints():
            self.cli.run()
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('task edit 1 name'))
            self.assertEqual(mock_command.call_count, 1)
            self.assertEqual(mock_passer.call_count, 1)

            self.cli.run()
            self.assertEqual(mock_command.call_count, 3)
            self.assertEqual(mock_passer.call_count, 2)

            self.cli.run()
            self.assertEqual(mock_command.call_count, 5)
            self.assertEqual(mock_passer.call_count, 3)

            self.cli.run()
            self.assertEqual(mock_command.call_count, 7)
            self.assertEqual(mock_passer.call_count, 4)

            self.cli.run()
            self.assertEqual(mock_command.call_count, 9)
            self.assertEqual(mock_passer.call_count, 5)

    @patch('src.modules.mumjolandia.cli.mumjolandia_cli.MumjolandiaCli._MumjolandiaCli__clear_screen', return_value=None)
    @patch('src.modules.mumjolandia.mumjolandia_data_passer.MumjolandiaDataPasser.pass_command', return_value=None)
    @patch('src.modules.console.console.Console.get_next_command',
           side_effect=[CommandFactory.get_command('cls'),
                        CommandFactory.get_command('needed_to_exit_loop'),
                        CommandFactory.get_command('path'),
                        CommandFactory.get_command('needed_to_exit_loop')])
    def test_calling_not_passable_commands_with_mode(self, mock_command, mock_passer, mock_cls):
        with HiddenPrints():
            self.cli.mode = MumjolandiaCliMode.task
            self.cli.run()
            self.assertEqual(mock_command.call_count, 2)
            self.assertEqual(mock_passer.call_count, 1)
            self.assertEqual(mock_cls.call_count, 1)

            self.cli.run()
            self.assertEqual(mock_command.call_count, 4)
            self.assertEqual(mock_passer.call_count, 2)
            self.assertEqual(mock_cls.call_count, 1)

    @patch('src.modules.mumjolandia.mumjolandia_data_passer.MumjolandiaDataPasser.pass_command', return_value=None)
    @patch('src.modules.console.console.Console.get_next_command',
           side_effect=[CommandFactory.get_command('exit')])
    def test_calling_exit_with_mode(self, mock_command, mock_passer):
        with HiddenPrints():
            self.cli.mode = MumjolandiaCliMode.task
            self.cli.run()
            self.assertEqual(mock_passer.call_args[0][0], CommandFactory.get_command('exit'))
            self.assertEqual(mock_command.call_count, 1)
            self.assertEqual(mock_passer.call_count, 1)
