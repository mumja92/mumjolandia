import datetime
import platform
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
