import logging

from src.interface.connection.message import Message


class MessageFactory:
    @staticmethod
    def get(data):
        max_message_size = 4294967295   # 4 bytes appended at the beginning of message
        if len(data) > max_message_size:
            return None
        if type(data) is bytes:
            return Message(data)
        if type(data) is str:
            return Message(data.encode('utf-8'))
        logging.error("Message creation failed")
        return None
