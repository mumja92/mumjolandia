import datetime
import logging
import threading


class Scheduler:
    @staticmethod
    def schedule_fixed(time_string, function, args):
        """
        Call 'function' at a time given by 'time_string'
        usage:
        def custom_function(*arg):
            print("im in " + str(arg[1]))
        Scheduler.schedule_fixed('2020-08-11 16:05:00', custom_function, ['abc', 5])

        :param time_string:
        format:     '%Y-%m-%d %H:%M:%S'
        ie.         '2020-08-20 16:05:00'
        :param function:
        :param args:
        :return:
        """
        try:
            date_time_obj = datetime.datetime.strptime(str(time_string), '%Y-%m-%d %H:%M:%S')
        except ValueError:
            logging.error('String conversion to \'datetime\' failed. Given string: ' + str(time_string))
            return None
        now = datetime.datetime.now()
        if date_time_obj > now:
            delta = (date_time_obj - now).seconds
        else:
            delta = 0
        threading.Timer(delta, function, args).start()

    @staticmethod
    def schedule_relative(seconds, function, args):
        """
        Call 'function' after given 'seconds'
        usage:
        def custom_function(*arg):
            print("im in " + str(arg[1]))
        Scheduler.schedule_relative(3.0, custom_function, ['abc', 5])

        :param seconds: float
        :param function:
        :param args: list
        :return:
        """
        threading.Timer(seconds, function, args).start()
