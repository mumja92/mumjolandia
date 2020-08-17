import os
import socket

import time

from src.modules.connection.message_factory import MessageFactory
from src.modules.mumjolandia.config_loader import ConfigLoader


class SocketClient:
    def __init__(self, address, port):
        self.address_client = address
        self.port_client = port
        self.socket_client = None

    def send_message(self, message):    # message = bytes or str
        print('Sending from: ' + str(self.address_client) + ':' + str(self.port_client))
        print('Sending to  : ' + str(ConfigLoader.get_config().server_address) + ':' + str(ConfigLoader.get_config().server_port))
        return_value = 'not known error'
        try:
            self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_client.settimeout(3)
            self.socket_client.connect((ConfigLoader.get_config().server_address,
                                        int(ConfigLoader.get_config().server_port)))
            m_to_send = MessageFactory().get(message)
            self.socket_client.send(m_to_send.get())
            return_value = MessageFactory.get(self.__receive_message()).get_string()
        except ConnectionResetError as e:
            return_value = str(e)
        except ConnectionRefusedError as e:
            return_value = str(e)
        except socket.timeout as e:
            return_value = 'connection timeout - ' + str(e)
        finally:
            self.socket_client.close()
            return return_value

    def get_mumjolandia_update_package(self, file_name='mumjolandia.tar.gz'):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((ConfigLoader.get_config().server_address,
                                    int(ConfigLoader.get_config().server_port)))
        m_to_send = MessageFactory().get('update')
        self.socket_client.send(m_to_send.get())
        bytes_received = self.__receive_message(log_progress=True)
        if os.path.isfile(file_name):
            os.remove(file_name)
        with open(file_name, 'wb') as f:
            f.write(bytes_received)
        self.socket_client.close()
        return os.path.abspath(file_name)

    def get_file(self, file_name):
        return_value = None
        if type(file_name) is not str:
            return None
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect((ConfigLoader.get_config().server_address,
                                    int(ConfigLoader.get_config().server_port)))
        m_to_send = MessageFactory().get('get ' + file_name)
        self.socket_client.send(m_to_send.get())
        bytes_received = self.__receive_message(log_progress=True)
        if len(bytes_received) > 0:
            if os.path.isfile(file_name):
                os.remove(file_name)
            with open(file_name, 'wb+') as f:
                f.write(bytes_received)
            return_value = os.path.abspath(file_name)
        self.socket_client.close()
        return return_value

    def __receive_message(self, log_progress=False):
        start_time = 0
        previous_bytes = 0
        len_bytes = b''
        while len(len_bytes) < 4:   # first 4 bytes are length of message
            len_bytes += self.socket_client.recv(1)
        bytes_received = b''
        if log_progress:
            print("Downloading " + str(float(int.from_bytes(len_bytes, byteorder='big', signed=False))/1024/1024) + 'MB')
            start_time = time.time()
        while len(bytes_received) < int.from_bytes(len_bytes, byteorder='big', signed=False):
            bytes_received += self.socket_client.recv(1024*1024)
            if log_progress:
                elapsed_time = time.time() - start_time
                if elapsed_time > 1:
                    self.__print_progress(len(bytes_received),
                                          int.from_bytes(len_bytes, byteorder='big', signed=False),
                                          " {0:.2f}".format((len(bytes_received) - previous_bytes)/1024/1024) + 'MB/s')
                    previous_bytes = len(bytes_received)
                    start_time += 1
        return bytes_received

    def __print_progress(self, current, target, speed):
        print(str(int(current/target*100)) + '% ' + speed)
