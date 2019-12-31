import logging
import os
import threading
from queue import Queue

from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.mumjolandia.mumjolandia_data_passer import MumjolandiaDataPasser
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.cli.mumjolandia_cli import MumjolandiaCli


class MumjolandiaStarter:
    def __init__(self, commands=None):
        self.commands = CommandFactory().get_command(commands)
        if self.commands is not None:
            self.commands.append(CommandFactory().get_command('exit'))
        self.config = ConfigLoader.get_config()
        self.log_location = 'data/log.log'
        self.command_queue_request = Queue()
        self.command_queue_response = Queue()
        self.command_responded_event = threading.Event()
        self.data_passer = None
        self.command_mutex = threading.Lock()
        self.mumjolandia_thread = None
        self.__run_init()

    def run_cli(self):
        logging.info('Starting CLI')
        self.__run_mumjolandia()
        cli = MumjolandiaCli(self.data_passer, self.commands)
        cli.setName('cli thread')
        cli.start()

    def set_commands(self, commands):
        self.commands = CommandFactory().get_command(commands)

    def get_mumjolandia_thread(self):
        return self.mumjolandia_thread

    def __run_mumjolandia(self):
        logging.info('Starting mumjolandia')
        self.mumjolandia_thread = MumjolandiaThread(self.command_queue_request,
                                                    self.command_queue_response,
                                                    self.command_responded_event)
        self.mumjolandia_thread.setName('mumjolandia thread')
        self.mumjolandia_thread.start()

    def __run_init(self):
        if not os.path.isdir("data"):
            try:
                os.mkdir("data")
            except OSError as e:
                pass
        try:
            if os.path.isfile(self.log_location):
                os.remove(self.log_location)
        except OSError as e:
            pass
        try:
            handlers = []
            if self.config.log_to_display.lower() == 'True'.lower():
                handlers.append(logging.StreamHandler())
            if self.config.log_to_file.lower() == 'True'.lower():
                handlers.append(logging.FileHandler(self.log_location))
            if len(handlers) == 0:
                logging.getLogger().disabled = True
            else:
                logging.basicConfig(format='%(asctime)s [%(levelname).1s] %(module)s::%(funcName)s --- %(message)s',
                                    datefmt='%d/%m/%Y %H:%M:%S', handlers=handlers, level=self.config.log_level.upper())
        except ValueError:
            logging.error('Logging level: "' + self.config.log_level + '" is incorrect.')
        self.data_passer = MumjolandiaDataPasser(self.command_queue_request,
                                                 self.command_queue_response,
                                                 self.command_mutex,
                                                 self.command_responded_event)
