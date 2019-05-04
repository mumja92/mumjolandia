from src.interface.connection.status import Status
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.external import paramiko


class ConnectionSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.status = None
        self.__init()

    def __init(self):
        self.__add_command_parsers()
        self.status = Status.not_connected

    def __add_command_parsers(self):
        self.command_parsers['help'] = self.__command_help

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_help,
                                         arguments=['pusto\n'
                                                    'tu[name]\n'])
