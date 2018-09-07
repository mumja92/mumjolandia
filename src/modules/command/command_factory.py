from src.modules.command.command import Command


class CommandFactory:
    @staticmethod
    def get_command(string):
        if len(string) == 0:
            arguments = ['']
            return Command(arguments)
        else:
            return Command(string.split())
