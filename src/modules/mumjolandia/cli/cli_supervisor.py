import os
import platform

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor


class CliSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        self.permanent_cls = False
        super().__init__()
        self.__add_command_parsers()

    def execute(self, command):
        if self.permanent_cls:
            self.__clear_screen()
        return super(CliSupervisor, self).execute(command)

    def __add_command_parsers(self):
        self.command_parsers['c'] = self.__command_c
        self.command_parsers['cls'] = self.__command_cls
        self.command_parsers['date'] = self.__command_date
        self.command_parsers['mode'] = self.__command_mode
        self.command_parsers['path'] = self.__command_path

    def __clear_screen(self):
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    def __command_c(self, args):
        self.permanent_cls = not self.permanent_cls
        if self.permanent_cls:
            self.__clear_screen()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.cli_handled, arguments=args)

    def __command_cls(self, args):
        self.__clear_screen()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.cli_handled, arguments=args)

    def __command_date(self, args):
        import datetime
        print('datetime.date.today:')
        print(datetime.date.today())
        from datetime import date
        import time
        print('date.fromtimestamp(time.time())')
        print(date.fromtimestamp(time.time()))
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.cli_handled, arguments=args)

    def __command_mode(self, args):
        if len(args) == 0:
            return_arguments = []
        else:
            return_arguments = [args[0]]
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.cli_mode, arguments=return_arguments)

    def __command_path(self, args):
        print('Script location: ' + os.path.dirname(os.path.realpath(__file__)))
        print('Working directory: ' + os.getcwd())
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.cli_handled, arguments=args)
