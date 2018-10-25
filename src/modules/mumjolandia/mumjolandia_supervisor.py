import logging
from queue import Queue

from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.ui.mumjolandia_cli import MumjolandiaCli
from src.modules.mumjolandia.ui.mumjolandia_gui import MumjolandiaGui


class MumjolandiaSupervisor:
    def __init__(self):
        self.command_queue_input = Queue()
        self.command_queue_output = Queue()
        self.command_queue_ui = Queue()  # not used yet todo: send exit command to cli
        logging.basicConfig(format='%(asctime)s [%(levelname).1s] %(module)s::%(funcName)s --- %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='spam.log', level=logging.DEBUG)

    def run_gui(self):
        logging.info('Starting GUI')
        self.__run_mumjolandia()
        gui = MumjolandiaGui(4)
        gui.run()
        self.__main_loop()

    def run_cli(self):
        logging.info('Starting CLI')
        self.__run_mumjolandia()
        cli = MumjolandiaCli(self.command_queue_input, self.command_queue_ui)
        cli.setName('cli thread')
        cli.start()
        self.__main_loop()

    def __run_mumjolandia(self):
        logging.info('Starting mumjolandia')
        mumjolandia_thread = MumjolandiaThread(self.command_queue_output)
        mumjolandia_thread.setName('mumjolandia thread')
        mumjolandia_thread.start()

    def __main_loop(self):
        while True:
            command_string = self.command_queue_input.get()
            self.command_queue_input.task_done()
            command = CommandFactory.get_command(command_string)
            logging.info('Parsing command: ' + str(command))
            self.command_queue_output.put(command)
            if command.arguments[0] == 'exit':
                logging.info('exiting')
                break
