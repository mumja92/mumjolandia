from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.ui.mumjolandia_cli import MumjolandiaCli
from src.modules.mumjolandia.ui.mumjolandia_gui import MumjolandiaGui
from queue import Queue


class MumjolandiaSupervisor:
    def __init__(self):
        self.command_queue = Queue()

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
