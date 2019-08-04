import os
import socket

from src.modules.connection.message_factory import MessageFactory
from src.modules.mumjolandia.config_loader import ConfigLoader


class SocketClient:
    def __init__(self, address, port):
        self.address_client = address
        self.port_client = port
        self.socket_client = None

    def send_message(self, message):    # message = bytes or str
        return_value = 'not known error'
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.settimeout(3)
            self.socket_client.connect((ConfigLoader.get_config().server_address,
                                        int(ConfigLoader.get_config().server_port)))
            m_to_send = MessageFactory().get(message)
            self.socket_client.send(m_to_send.get())
            return_value = MessageFactory.get(self.__receive_message()).get_string()
        except ConnectionResetError:
            return_value = 'connection broken'
        except ConnectionRefusedError:
            return_value = 'connection refused'
        except socket.timeout:
            return_value = 'connection timeout'
        finally:
            self.socket_client.close()
            return return_value

    def get_mumjolandia_update_package(self, file_name='mumjolandia.tar.gz'):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((ConfigLoader.get_config().server_address,
                                    int(ConfigLoader.get_config().server_port)))
        m_to_send = MessageFactory().get('update')
        self.socket_client.send(m_to_send.get())
        bytes_received = self.__receive_message()
        if os.path.isfile(file_name):
            os.remove(file_name)
        with open(file_name, 'wb') as f:
            f.write(bytes_received)
        self.socket_client.close()
        return os.path.abspath(file_name)

    def __receive_message(self):
        len_bytes = b''
        while len(len_bytes) < 4:   # first 4 bytes are length of message
            len_bytes += self.socket_client.recv(1)
        bytes_received = b''
        while len(bytes_received) < int.from_bytes(len_bytes, byteorder='big', signed=False):
            bytes_received += self.socket_client.recv(1024)
        return bytes_received
