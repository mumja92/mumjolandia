import logging
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.ui.mumjolandia_cli import MumjolandiaCli
from src.modules.mumjolandia.ui.mumjolandia_gui import MumjolandiaGui
from queue import Queue


class MumjolandiaSupervisor:
    def __init__(self):
        self.command_queue = Queue()
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%d/%m/%Y %H:%M:%S;', filename='spam.log', level=logging.DEBUG)
        logging.debug('This message should go to the log file')
        logging.info('So should this')
        logging.warning('And this, too')

    def run_gui(self):
        self.__run_mumjolandia()
        gui = MumjolandiaGui(4)
        gui.run()

    def run_cli(self):
        self.__run_mumjolandia()
        cli = MumjolandiaCli(self.command_queue)
        cli.setName('cli thread')
        cli.start()

    def __run_mumjolandia(self):
        mumjolandia_thread = MumjolandiaThread(self.command_queue)
        mumjolandia_thread.setName('mumjolandia thread')
        mumjolandia_thread.start()
