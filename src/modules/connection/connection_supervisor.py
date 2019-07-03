from src.interface.connection.status import Status
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.connection.socket_client import SocketClient
from src.modules.connection.socket_server import SocketServer


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
        self.command_parsers['server'] = self.__command_server_start
        self.command_parsers['send'] = self.__command_client_send

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_help,
                                         arguments=['pusto\n'
                                                    'tu[name]\n'])

    def __command_server_start(self, args):
        address = 'localhost'
        port = 3333
        s = SocketServer(address, port)
        s.run_once()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_server_start,
                                         arguments=['done'])

    def __command_client_send(self, args):
        address = 'localhost'
        port = 3333
        s = SocketClient(address, port)
        return_value = s.send_message(str(args[0]))
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_client_send_ok,
                                         arguments=[return_value])
