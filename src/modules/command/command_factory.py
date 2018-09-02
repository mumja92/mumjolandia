from src.modules.command.command import Command


class CommandFactory:
    @staticmethod
    def get_command(string):
        return Command(string.split())
