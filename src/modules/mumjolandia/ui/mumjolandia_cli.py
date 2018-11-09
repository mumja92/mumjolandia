import logging
import os
import platform
from threading import Thread

from src.interface.mumjolandia.mumjolandia_cli_mode import MumjolandiaCliMode
from src.interface.mumjolandia.mumjolandia_immutable_type_wrapper import MumjolandiaImmutableTypeWrapper
from src.modules.console.console import Console
from src.modules.mumjolandia.ui.mumjolandia_cli_printer import MumjolandiaCliPrinter


class MumjolandiaCli(Thread):
    def __init__(self, data_passer):
        Thread.__init__(self)
        self.console = Console()
        self.data_passer = data_passer
        self.exit_flag = MumjolandiaImmutableTypeWrapper(False)
        self.cli_printer = MumjolandiaCliPrinter(self.exit_flag)
        self.mode = MumjolandiaCliMode.none

    def __del__(self):
        logging.info('mumjolandia cli exiting')

    def run(self):
        logging.info('mumjolandia cli started')
        while True:
            print(self.__get_prompt(), end='')
            command = self.console.get_next_command()
            if not self.__prepare_command(command):
                continue
            return_value = self.data_passer.pass_command(command)
            self.cli_printer.execute(return_value)
            if self.exit_flag.object:
                break

    def __prepare_command(self, command):
        if command.arguments[0] == 'mode':
            if len(command.arguments) == 1:
                self.mode = MumjolandiaCliMode.none
                return False
            try:
                self.mode = MumjolandiaCliMode[command.arguments[1]]
            except KeyError:
                print('Unrecognized mode: ' + command.arguments[1])
            return False

        if self.mode != MumjolandiaCliMode.none:
            command.arguments.insert(0, self.mode.name)

        if command.arguments[0] == 'cls':
            self.__clear_screen()
            return False

        if command.arguments[0] == 'path':
            print('Script location: ' + os.path.dirname(os.path.realpath(__file__)))
            print('Working directory: ' + os.getcwd())
            return False

        if command.arguments[0:2] == ['task', 'print']:
            command.arguments[1] = 'get'

        if command.arguments[0:2] == ['task', 'edit']:
            try:
                int(command.arguments[2])
            except (ValueError, IndexError):
                print('id is not a number')
                print('usage: "task edit [id] [name]')
                return False
            try:
                if len(command.arguments[3]) < 1:
                    print('Name should have at least 1 character')
                    print('usage: "task edit [id] [name]')
                    return False
            except IndexError:
                print('Name should have at least 1 character')
                print('usage: "task edit [id] [name]')
                return False
        return True

    def __clear_screen(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def __get_prompt(self):
        if self.mode == MumjolandiaCliMode.none:
            return 'mumjolandia>'
        else:
            return 'mumjolandia/' + self.mode.name + '>'
