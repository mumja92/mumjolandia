import socket

from src.modules.connection.message_factory import MessageFactory


class SocketServer:
    def __init__(self, address, port):
        self.address_server = address
        self.port_server = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.address_server, self.port_server))

    def run_once(self):
        self.server_socket.listen(1)
        connect, address = self.server_socket.accept()
        print("Connection Address:" + str(address))
        received_message = self.__get_message_object(connect)
        print(received_message.get_string())
        msg_return = MessageFactory().get(received_message.get_string())
        self.__send_message_object(msg_return, connect, address)
        connect.close()

    def run_session(self):
        self.server_socket.listen(1)
        connect, address = self.server_socket.accept()
        print("Connection Address:" + str(address))
        while True:
            received_message = self.__get_message_object(connect)
            print(received_message.get_string())
            msg_return = MessageFactory().get(received_message.get_string())
            if received_message.get_string() == 'exit':
                print('exiting')
                self.__send_string('bye', connect, address)
                break
            else:
                print('sending: ' + msg_return.get_string())
                self.__send_message_object(msg_return, connect, address)
        connect.close()

    def __get_message_object(self, connection):
        received_len = int.from_bytes(connection.recv(4), byteorder='big', signed=False)
        received_message = MessageFactory().get(connection.recv(received_len))
        return received_message

    def __send_message_object(self, message, connection, address):
        msg_return = MessageFactory().get(message.get_string())
        connection.sendto(msg_return.get(), address)

    def __send_string(self, string, connection, address):
        msg_return = MessageFactory().get(string)
        connection.sendto(msg_return.get(), address)
