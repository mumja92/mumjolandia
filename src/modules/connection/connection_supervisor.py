from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.connection.socket_client import SocketClient
from src.modules.connection.socket_server import SocketServer
from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.mumjolandia.mumjolandia_updater import MumjolandiaUpdater


class ConnectionSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['server'] = self.__command_server_start
        self.command_parsers['send'] = self.__command_client_send
        self.command_parsers['update'] = self.__command_update
        self.command_parsers['get'] = self.__command_get

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_help,
                                         arguments=['server\n'
                                                    'server [x] (session)\n'
                                                    'send [msg]\n'
                                                    'send exit (shutdown server)\n'
                                                    'get [filename] \n'
                                                    'update\n'])

    def __command_server_start(self, args):
        s = SocketServer('0.0.0.0', int(ConfigLoader.get_config().server_port))
        if len(args) > 0:
            s.run()
        else:
            s.run_once()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_server_start,
                                         arguments=['done'])

    def __command_client_send(self, args):
        try:
            s = SocketClient(ConfigLoader.get_config().server_address, int(ConfigLoader.get_config().server_port))
            return_value = s.send_message(str(args[0]))
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_client_send_ok,
                                             arguments=[return_value])
        except ConnectionRefusedError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_failed,
                                             arguments=['Can\'t connect to server'])

    def __command_update(self, args):
        try:
            s = SocketClient(ConfigLoader.get_config().server_address, int(ConfigLoader.get_config().server_port))
            path = s.get_mumjolandia_update_package('mumjolandia.tar.gz')
            MumjolandiaUpdater.install_source(path)
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_client_send_ok,
                                             arguments=['ok'])
        except ConnectionRefusedError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_failed,
                                             arguments=['Can\'t connect to server'])

    def __command_get(self, args):
        try:
            s = SocketClient(ConfigLoader.get_config().server_address, int(ConfigLoader.get_config().server_port))
            path = s.get_file(args[0])
            if path is None:
                return_value = 'Connection ok, but received file empty'
            else:
                return_value = 'received file: ' + path
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_client_send_ok,
                                             arguments=[return_value])
        except ConnectionRefusedError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_failed,
                                             arguments=['Can\'t connect to server'])
