import logging
import os
import platform
from threading import Thread

import time

from src.interface.mumjolandia.mumjolandia_cli_mode import MumjolandiaCliMode
from src.interface.mumjolandia.mumjolandia_immutable_type_wrapper import MumjolandiaImmutableTypeWrapper
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.command.command_factory import CommandFactory
from src.modules.console.console import Console
from src.modules.mumjolandia.cli.cli_supervisor import CliSupervisor
from src.modules.mumjolandia.cli.mumjolandia_cli_printer import MumjolandiaCliPrinter


class MumjolandiaCli(Thread):
    def __init__(self, data_passer, commands=None):
        Thread.__init__(self)
        self.exit_flag = False
        self.cli_printer = MumjolandiaCliPrinter()
        self.cli_supervisor = CliSupervisor()
        self.commands = commands
        self.console = Console()
        self.data_passer = data_passer
        self.mode = MumjolandiaCliMode.none
        self.permanent_cls = False

    def __del__(self):
        logging.info('mumjolandia cli exiting')

    def run(self):
        logging.info('mumjolandia cli started')
        if self.commands is None:
            while True:
                print(self.__get_prompt(), end='')
                command = self.console.get_next_command()
                self.__handle_command(command)
                if self.exit_flag:
                    break
        else:
            for c in self.commands:
                self.__handle_command(c)

    def __handle_command(self, command):
        cli_response = self.cli_supervisor.execute(command)
        if cli_response.status == MumjolandiaReturnValue.cli_handled:
            return
        elif cli_response.status == MumjolandiaReturnValue.cli_mode:
            if len(cli_response.arguments) == 0:
                self.mode = MumjolandiaCliMode.none
                return
            try:
                self.mode = MumjolandiaCliMode[command.arguments[1]]
            except KeyError:
                print('Unrecognized mode: ' + str(command.arguments[1]))
        else:
            if self.mode != MumjolandiaCliMode.none:
                if command.arguments[0] != 'exit':
                    command.arguments.insert(0, self.mode.name)
            return_value = self.data_passer.pass_command(command)
            self.cli_printer.execute(return_value)
            if return_value.status == MumjolandiaReturnValue.mumjolandia_exit:
                self.exit_flag = True

    def __prepare_command(self, command):
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

        if command.arguments[0:2] == ['note', 'print']:
            command.arguments[1] = 'get'

        if command.arguments[0:2] == ['task', 'print']:
            command.arguments[1] = 'get'

        if command.arguments[0:2] == ['game', 'print']:
            command.arguments[1] = 'get'

        if command.arguments[0:2] == ['event', 'print']:
            command.arguments[1] = 'get'

        if command.arguments[0:2] == ['weather', 'print']:
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

    def __get_prompt(self):
        if self.mode == MumjolandiaCliMode.none:
            return 'mumjolandia>'
        else:
            return 'mumjolandia/' + self.mode.name + '>'
