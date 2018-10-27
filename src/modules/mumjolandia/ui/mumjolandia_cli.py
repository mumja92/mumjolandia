import logging
from threading import Thread
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
            self.__pass_command(command)
            if self.__command_exit(command):
                break
        logging.info('mumjolandia cli exiting')

    def __pass_command(self, command):
        self.data_passer.pass_command(command)

    def __command_exit(self, command):
        if command.arguments[0] == "exit":
            return True
        return False
