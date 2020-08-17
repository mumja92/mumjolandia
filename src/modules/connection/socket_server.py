import os
import socket

from src.modules.connection.message_factory import MessageFactory
from src.modules.connection.remote_command_executor import RemoteCommandExecutor
from src.modules.mumjolandia.mumjolandia_updater import MumjolandiaUpdater


class SocketServer:
    def __init__(self, address, port):
        self.port_server = port
        self.address_server = address
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.remote_command_executor = RemoteCommandExecutor()

        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind((self.address_server, self.port_server))

    def run_once(self):
        print('Server up: ' + str(self.address_server) + ':' + str(self.port_server))
        self.socket_server.listen(1)
        connect, address = self.socket_server.accept()
        print("Connection Address:" + str(address))
        received_message = MessageFactory.get(self.__receive_message(connect))
        print(received_message.get_string())
        msg_return = self.__parse_message(received_message)
        self.__send_message_object(msg_return, connect, address)
        connect.close()

    def run(self):
        print('Server up: ' + str(self.address_server) + ':' + str(self.port_server))
        while True:
            self.socket_server.listen(1)
            connect, address = self.socket_server.accept()
            print(address[0] + ':' + str(address[1]), end=': ')
            try:
                received_message = MessageFactory.get(self.__receive_message(connect))
                print(received_message.get_string())
                if received_message.get_string() == 'exit':
                    print('exiting')
                    self.__send_string('bye', connect, address)
                    break
                else:
                    msg_return = self.__parse_message(received_message)
                    self.__send_message_object(msg_return, connect, address)
            except socket.error as e:
                print(str(e))
            connect.close()

    def __parse_message(self, message):
        if message.get_string() == 'update':
            update_file = MumjolandiaUpdater.pack_source()
            with open(update_file, 'rb') as f:
                data = f.read()
            os.remove(update_file)
            msg_return = MessageFactory().get(data)
        elif message.get_string().startswith('get '):
            if os.path.isfile(message.get_string()[4:]):
                with open(message.get_string()[4:], 'rb') as f:
                    data = f.read()
                msg_return = MessageFactory().get(data)
            else:
                msg_return = MessageFactory().get('')
        else:
            msg_return = MessageFactory().get(self.remote_command_executor.execute(message.get_string()))
        return msg_return

    def __send_message_object(self, message, connection, address):
        connection.sendto(message.get(), address)

    def __send_string(self, string, connection, address):
        msg_return = MessageFactory().get(string)
        connection.sendto(msg_return.get(), address)

    def __receive_message(self, connection):
        len_bytes = b''
        while len(len_bytes) < 4:   # first 4 bytes are length of message
            len_bytes += connection.recv(1)
        bytes_received = b''
        while len(bytes_received) < int.from_bytes(len_bytes, byteorder='big', signed=False):
            bytes_received += connection.recv(1024)
        return bytes_received
