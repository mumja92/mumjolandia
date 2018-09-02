from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.ui.mumjolandia_gui import MumjolandiaGui


class Mumjolandia:
    def __init__(self):
        pass

    def run_gui(self):
        self.__run_mumjolandia()
        gui = MumjolandiaGui(4)
        gui.run()

    def run_cli(self):
        # self.run_mumjolandia()
        pass

    def __run_mumjolandia(self):
        mumjolandia_thread = MumjolandiaThread(4)
        mumjolandia_thread.setName('mumjolandia thread')
        mumjolandia_thread.start()
