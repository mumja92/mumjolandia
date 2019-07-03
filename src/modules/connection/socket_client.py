import socket

from src.interface.connection.message import Message
from src.modules.connection.message_factory import MessageFactory


class SocketClient:
    def __init__(self, address, port):
        self.address_client = address
        self.port_client = port
        self.socket_client = None

    def send_message(self, message):    # message = bytes or str
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect(("localhost", 3333))
        m_to_send = MessageFactory().get(message)
        self.socket_client.send(m_to_send.get())
        received_len = int.from_bytes(self.socket_client.recv(4), byteorder='big', signed=False)
        m_received = Message(self.socket_client.recv(received_len))
        self.socket_client.close()
        return m_received.get_string()

    def send_session(self):
        self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_client.connect(("localhost", 3333))
        while True:
            m_to_send = MessageFactory().get(input())
            self.socket_client.send(m_to_send.get())
            received_len = int.from_bytes(self.socket_client.recv(4), byteorder='big', signed=False)
            m_received = Message(self.socket_client.recv(received_len))
            print('got: ' + m_received.get_string())
            x = m_received.get_string()
            if m_received.get_string() == 'bye':
                print('exiting')
                break
        self.socket_client.close()