import logging
import os
import threading
from queue import Queue

import time

from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.mumjolandia.mumjolandia_data_passer import MumjolandiaDataPasser
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.ui.cli.mumjolandia_cli import MumjolandiaCli
from src.modules.mumjolandia.ui.server.mumjolandia_server import MumjolandiaServer


class MumjolandiaStarter:
    def __init__(self, sysargs):
        self.commands = None
        self.__init_commands(sysargs[1:])       # rest of arguments are user passed commands
        self.config = ConfigLoader.get_config()
        self.log_location = ConfigLoader.get_mumjolandia_location() + 'data/log.log'
        self.command_queue_request = Queue()
        self.command_queue_response = Queue()
        self.command_responded_event = threading.Event()
        self.data_passer = None
        self.command_mutex = threading.Lock()
        self.mumjolandia_thread = None
        self.__run_init()

    def run(self):
        self.__run_mumjolandia()
        if ConfigLoader.get_config().background_server == 'true':
            self.run_server()
        self.run_cli()

    def run_cli(self):
        cli = MumjolandiaCli(self.data_passer, self.commands)
        cli.setName('cli thread')
        cli.start()

    def run_server(self):
        server = MumjolandiaServer(self.data_passer)
        server.setName('mumjolandia server')
        server.start()

    def get_mumjolandia_thread(self):
        return self.mumjolandia_thread

    def set_commands(self, commands):
        self.commands = CommandFactory().get_command(commands)
        self.commands.append(CommandFactory().get_command('exit'))

    def __run_mumjolandia(self):
        self.mumjolandia_thread = MumjolandiaThread(self.command_queue_request,
                                                    self.command_queue_response,
                                                    self.command_responded_event)
        self.mumjolandia_thread.setName('mumjolandia thread')
        self.mumjolandia_thread.start()

    def __run_init(self):
        if not os.path.isdir(ConfigLoader.get_mumjolandia_location() + "data"):
            try:
                os.mkdir(ConfigLoader.get_mumjolandia_location() + "data")
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

    def __init_commands(self, commands):
        self.commands = CommandFactory().get_command(commands)
        if not len(self.commands):
            self.commands = None
        if self.commands is not None:
            self.commands.append(CommandFactory().get_command('exit'))
