import shutil
import textwrap

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.utils.polish_utf_to_ascii import PolishUtfToAscii


class UtilsSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):

        self.command_parsers['help'] = self.__command_help
        self.command_parsers['ip'] = self.__command_ip
        self.command_parsers['location'] = self.__command_location
        self.command_parsers['l'] = self.__command_location

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_help,
                                         arguments=['ip\n'
                                                    '[l]ocation\n'
                                                    ])

    def __command_ip(self, args):
        # todo: use 'with' statement and handle exceptions
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_get,
                                         arguments=[str(ip_address)])

    def __command_location(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_get,
                                         arguments=[ConfigLoader.get_mumjolandia_location()])
