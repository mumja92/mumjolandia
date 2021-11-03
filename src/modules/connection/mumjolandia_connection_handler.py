import logging

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.utils.rootfs_manager import RootFSManager
from src.modules.connection.remote_command_executor import RemoteCommandExecutor
from src.utils.socket.socket_client import SocketClient
from src.utils.socket.socket_server import SocketServer


class MumjolandiaConnectionHandler:
    def __init__(self, port, server_address=None, server_accepted_networks_mask="0.0.0.0"):
        self.port = int(port)
        self.server_address = server_address
        self.server_accepted_networks_mask = server_accepted_networks_mask

        self.server_loop_exit_flag = None

        self.rootfs_manager = RootFSManager()

    def start_server(self, run_once=True):
        logging.debug('Starting server; ' + self.server_accepted_networks_mask + ":" + str(self.port))
        self.server_loop_exit_flag = run_once
        try:
            while True:
                with SocketServer(self.server_accepted_networks_mask, self.port) as server:
                    received_message = server.receive()
                    logging.debug("Received: " + '"' + received_message + '"')
                    response_message = self.__parse_received_message(received_message)
                    server.send(response_message)
                if self.server_loop_exit_flag:
                    logging.debug("Server exited; " + self.server_accepted_networks_mask + ":" + str(self.port))
                    break
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_server_start,
                                             arguments=['done'])
        except Exception as e:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_server_start_fail,
                                             arguments=[str(e)])

    def send_message(self, message):
        logging.debug('Sending: "' + message + '" to ' + self.server_address + ":" + str(self.port))
        try:
            with SocketClient(self.server_address, int(self.port)) as s:
                return_value = s.send(str(message))
                logging.debug('Received: "' + return_value + '" from ' + self.server_address + ":" + str(self.port))
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_client_send_ok,
                                                 arguments=[return_value])
        except Exception as e:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.connection_failed,
                                             arguments=['Can\'t connect to server: ' + str(e)])

    def __parse_received_message(self, message):
        return_value = 'error'
        if message == 'exit':
            self.server_loop_exit_flag = True
            return_value = 'closing server'
        # this is not tested
        # elif message == 'update':
        #     update_file = MumjolandiaUpdater.pack_source()
        #     with open(update_file, 'rb') as f:
        #         data = f.read()
        #     os.remove(update_file)
        #     msg_return = MessageFactory().get(data)     # this is message what to do with it? monkaS
        # # not tested
        # elif message.startswith('get '):
        #     if os.path.isfile(message.get_string()[4:]):
        #         with open(message.get_string()[4:], 'rb') as f:
        #             data = f.read()
        #         msg_return = MessageFactory().get(data)
        #     else:
        #         msg_return = MessageFactory().get('')
        elif message == 'pwd':
            return_value = self.rootfs_manager.pwd()
        elif message.startswith('ls'):
            return_value = self.rootfs_manager.ls(message[3:])
            if return_value is None:
                return_value = "directory doesn't exist"
        elif message.startswith('cd'):
            if len(message) > 3:
                return_value = self.rootfs_manager.cd(message[3:])
            else:
                return_value = self.rootfs_manager.cd()
        else:
            return_value = RemoteCommandExecutor().execute(message)
        return return_value
