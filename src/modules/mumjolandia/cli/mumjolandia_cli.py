import logging
import os
import platform
from threading import Thread

from src.interface.mumjolandia.mumjolandia_cli_mode import MumjolandiaCliMode
from src.interface.mumjolandia.mumjolandia_immutable_type_wrapper import MumjolandiaImmutableTypeWrapper
from src.modules.console.console import Console
from src.modules.mumjolandia.cli.mumjolandia_cli_printer import MumjolandiaCliPrinter


class MumjolandiaCli(Thread):
    def __init__(self, data_passer):
        Thread.__init__(self)
        self.console = Console()
        self.data_passer = data_passer
        self.exit_flag = MumjolandiaImmutableTypeWrapper(False)
        self.cli_printer = MumjolandiaCliPrinter(self.exit_flag)
        self.mode = MumjolandiaCliMode.none
        self.permanent_cls = False

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
            if self.permanent_cls:
                self.__clear_screen()
            self.cli_printer.execute(return_value)
            if self.exit_flag.object:
                break

    def __prepare_command(self, command):
        self.__shortcut_generator(command)

        if command.arguments[0] == 'date':  # to delete later
            import datetime
            print('datetime.date.today:')
            print(datetime.date.today())
            from datetime import date
            import time
            print('date.fromtimestamp(time.time())')
            print(date.fromtimestamp(time.time()))
            return False

        if command.arguments[0] == 'help':
            print('Available commands:')
            print('fat, task, food, game, mode, cls, path, date, c')
            return False

        if command.arguments[0] == 'cls':
            self.__clear_screen()
            return False

        if command.arguments[0] == 'c':
            self.permanent_cls = not self.permanent_cls
            return False

        if command.arguments[0] == 'path':
            print('Script location: ' + os.path.dirname(os.path.realpath(__file__)))
            print('Working directory: ' + os.getcwd())
            return False

        if command.arguments[0] == 'exit':
            return True

        if command.arguments[0] == 'mode' or command.arguments[0] == 'm':
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

        if command.arguments[0:2] == ['fat', 'print']:
            command.arguments[1] = 'get'

        if command.arguments[0:2] == ['task', 'print']:
            command.arguments[1] = 'get'

        if command.arguments[0:2] == ['game', 'print']:
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

    def __shortcut_generator(self, command):
        try:
            if self.mode is not MumjolandiaCliMode.none:
                if command.arguments[0] == 'h':
                    command.arguments[0] = 'help'
                if command.arguments[0] == 'ls':
                    command.arguments[0] = 'print'
                if command.arguments[0] == 'rm':
                    command.arguments[0] = 'delete'
                if command.arguments[0] == 'h':
                    command.arguments[0] = 'help'
                if command.arguments[0] == 'i':
                    command.arguments[0] = 'ingredient'
        except IndexError:
            pass
        try:
            if command.arguments[0] == 't':
                command.arguments[0] = 'task'
            if command.arguments[0] == 'fo':
                command.arguments[0] = 'food'
            if command.arguments[0] == 'fa':
                command.arguments[0] = 'fat'
            if command.arguments[0] == 'h':
                command.arguments[0] = 'help'
            if command.arguments[1] == 'ls':
                command.arguments[1] = 'print'
            if command.arguments[1] == 'rm':
                command.arguments[1] = 'delete'
            if command.arguments[1] == 'h':
                command.arguments[1] = 'help'
            if command.arguments[1] == 'i':
                command.arguments[1] = 'ingredient'
        except IndexError:
            pass
