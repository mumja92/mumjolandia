import logging

from src.external.pydes.pydes import des


class PydesWrapper:
    def __init__(self):
        self.des = des()

    def encrypt(self, password, value):
        if not isinstance(password, str) or len(password) < 8:
            try:
                return_password = str(password)
            except ValueError:
                return_password = "<str(password) failed>"
            logging.warning('Received password (' + return_password + ') is incorrect')
            return None
        if not isinstance(value, str) or len(value) < 1:
            try:
                return_value = str(value)
            except ValueError:
                return_value = "<str(value) failed>"
            logging.warning('Received data (' + return_value + ') is incorrect')
            return None
        try:
            ciphered = self.des.encrypt(password, value, padding=True)
        except TypeError as e:
            logging.warning(str(e.args[0]))
            return None
        return ciphered

    def decrypt(self, password, value):
        if not isinstance(password, str) or len(password) < 8:
            try:
                return_password = str(password)
            except ValueError:
                return_password = "<str(password) failed>"
            logging.warning('Received password (' + return_password + ') is incorrect')
            return None
        if not isinstance(value, str) or len(value) < 1:
            try:
                return_value = str(value)
            except ValueError:
                return_value = "<str(value) failed>"
            logging.warning('Received data (' + return_value + ') is incorrect')
            return None
        try:
            deciphered = self.des.decrypt(password, value, padding=True)
        except TypeError as e:
            logging.warning(str(e.args[0]))
            return None
        return deciphered
