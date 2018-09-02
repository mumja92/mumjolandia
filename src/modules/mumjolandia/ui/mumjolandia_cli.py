from src.modules.console.console import Console


class MumjolandiaGui():
    def __init__(self, val):
        self.arg = val
        self.console = Console()

    def run(self):
        while True:
            print(' ')
            command = self.console.get_next_text()
            self.__pass_command(command)

    def __pass_command(self, command):
        # todo: pass command to mumjolandia
        pass
