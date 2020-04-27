from src.modules.command.command_factory import CommandFactory


class MumjolandiaHomepage:
    def __init__(self, data_passer):
        self.data_passer = data_passer

    def print(self):
        if not self.is_printable():
            return None
        print(self.__execute_mumjolandia_command('fat ls').arguments[-1])

    def is_printable(self):
        return False

    def __execute_mumjolandia_command(self, command):
        return self.data_passer.pass_command(CommandFactory().get_command(command))
