import socket

from src.modules.connection.message_factory import MessageFactory


class SocketServer:
    def __init__(self, address, port):
        self.port_server = port
        self.address_server = address
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket_server.bind((self.address_server, self.port_server))

    def run_once(self):
        self.socket_server.listen(1)
        connect, address = self.socket_server.accept()
        print("Connection Address:" + str(address))
        received_message = self.__get_message_object(connect)
        print(received_message.get_string())
        msg_return = MessageFactory().get(received_message.get_string())
        self.__send_message_object(msg_return, connect, address)
        connect.close()

    def run_session(self):
        self.socket_server.listen(1)
        connect, address = self.socket_server.accept()
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
