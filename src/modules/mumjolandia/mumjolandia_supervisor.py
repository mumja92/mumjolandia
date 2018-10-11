import logging
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.ui.mumjolandia_cli import MumjolandiaCli
from src.modules.mumjolandia.ui.mumjolandia_gui import MumjolandiaGui
from queue import Queue


class MumjolandiaSupervisor:
    def __init__(self):
        self.command_queue = Queue()
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%d/%m/%Y %H:%M:%S', filename='spam.log', level=logging.DEBUG)
        logging.debug('This message should go to the log file')

    def run_gui(self):
        logging.info('Starting GUI')
        self.__run_mumjolandia()
        gui = MumjolandiaGui(4)
        gui.run()

    def run_cli(self):
        logging.info('Starting CLI')
        self.__run_mumjolandia()
        cli = MumjolandiaCli(self.command_queue)
        cli.setName('cli thread')
        cli.start()

    def __run_mumjolandia(self):
        logging.info('Starting mumjolandia')
        mumjolandia_thread = MumjolandiaThread(self.command_queue)
        mumjolandia_thread.setName('mumjolandia thread')
        mumjolandia_thread.start()
