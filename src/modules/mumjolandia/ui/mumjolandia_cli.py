import logging
from threading import Thread

import sys

from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.console.console import Console


class MumjolandiaCli(Thread):
    def __init__(self, data_passer):
        Thread.__init__(self)
        self.console = Console()
        self.data_passer = data_passer

    def run(self):
        logging.info('mumjolandia cli started')
        while True:
            command = self.console.get_next_command()
            self.__execute_command(command)
            if self.__command_exit(command):
                break
        logging.info('mumjolandia cli exiting')

    def __execute_command(self, command):
        return_value = self.data_passer.pass_command(command)
        if return_value.status == MumjolandiaReturnValue.unrecognized_command:
            print('Unrecognized command: ', command.arguments, sep=' ', end='\n', file=sys.stdout, flush=False)
        elif return_value.status == MumjolandiaReturnValue.task_print:
            print(len(return_value.arguments), 'items:')
            for t in return_value.arguments:
                print(str(t))
        elif return_value.status == MumjolandiaReturnValue.task_added:
            print('Added: ' + str(return_value.arguments[0]))
        elif return_value.status == MumjolandiaReturnValue.task_incorrect_date_format:
            print('Incorrect date format')
        else:
            print('Unrecognized status response: ' + return_value.status.name)
            logging.error("Unrecognized status response: '" + return_value.status.name + "'")

    def __command_exit(self, command):
        if command.arguments[0] == "exit":
            return True
        return False
