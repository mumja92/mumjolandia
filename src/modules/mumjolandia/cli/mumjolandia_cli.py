import logging
import platform

from threading import Thread
from src.interface.mumjolandia.mumjolandia_cli_mode import MumjolandiaCliMode
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
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
                if self.exit_flag:
                    break
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
            if self.mode != MumjolandiaCliMode.none and return_value.status == MumjolandiaReturnValue.mumjolandia_unrecognized_parameters:
                del(command.arguments[0])
                mode_none_return_value = self.data_passer.pass_command(command)
                if mode_none_return_value != MumjolandiaReturnValue.mumjolandia_unrecognized_command:
                    return_value = mode_none_return_value
            self.cli_printer.execute(return_value)
            if return_value.status == MumjolandiaReturnValue.mumjolandia_exit:
                self.exit_flag = True

    def __get_prompt(self):
        prompt = ""
        if platform.system() != 'Windows':
            prompt += "\033[92m"
        if self.mode == MumjolandiaCliMode.none:
            prompt += 'mumjolandia>'
        else:
            prompt += 'mumjolandia/' + self.mode.name + '>'

        if platform.system() != 'Windows':
            prompt += "\033[0m"
        return prompt
