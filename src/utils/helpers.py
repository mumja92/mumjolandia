import datetime
import logging
import platform
import socket
import os


# todo: refactor a whole project to use this method
# todo: merge with helpers from ut


class DateHelper:
    @staticmethod
    def get_today_short(shift_days=0):  # only year-month-day
        return datetime.date.today() + datetime.timedelta(days=int(shift_days))

    @staticmethod
    def get_today_long(shift_days=0):  # y-m-d-h-s-ms
        return (datetime.datetime.today() + datetime.timedelta(days=int(shift_days))).replace(microsecond=0)


class RandomUtils:
    @staticmethod
    def clear_screen():
        if platform.system() == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def get_platform():
        """
        returns:
        'windows'
        'linux'
        'android'
        'unrecognized'
        """
        # On Android sys.platform returns 'linux2', so prefer to check the
        # presence of python-for-android environment variables (ANDROID_ARGUMENT
        # or ANDROID_PRIVATE).
        if 'ANDROID_ARGUMENT' in os.environ:
            return 'android'
        elif platform.system() == 'Windows':
            return 'windows'
        elif platform.system() == 'Linux':
            return 'linux'
        else:
            logging.warning('Unrecognized platform: ' + platform.system())
            return 'unrecognized'

    @staticmethod
    def get_ip():
        # todo: use 'with' statement and handle exceptions
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
