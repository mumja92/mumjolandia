from src.interface.password.password import Password
from src.utils.pydes_wrapper import PydesWrapper


class PasswordFactory:
    @staticmethod
    def get_password(password_to_encrypt_with, password_to_encrypt, name, username=None):
        return_password = PydesWrapper().encrypt(password_to_encrypt_with, password_to_encrypt)
        return_username = None
        if return_password is None:
            return None
        if username is not None:
            return_username = PydesWrapper().encrypt(password_to_encrypt_with, username)
        if return_username is None:
            return None
        return Password(str(name), return_username, return_password)
