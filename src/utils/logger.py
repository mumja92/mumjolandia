import logging
import os

from src.interface.utils.log_level import LogLevel


class Logger:
    print_to_display_flag = True
    log_location = None
    log_level = None

    def __init__(self, log_location, log_level_string, print_to_display):
        Logger.log_location = log_location
        Logger.log_level = Logger.__parse_log_level(log_level_string)
        if print_to_display.lower() == 'True'.lower():
            Logger.print_to_display_flag = True
        else:
            Logger.print_to_display_flag = False
        try:
            if os.path.isfile(Logger.log_location):
                os.remove(Logger.log_location)
        except OSError as e:
            pass
        try:
            logging.basicConfig(format='%(asctime)s [%(levelname).1s] %(module)s::%(funcName)s --- %(message)s',
                                datefmt='%d/%m/%Y %H:%M:%S', filename=Logger.log_location, level=Logger.log_level)
        except ValueError:
            logging.error('Logging level: "' + self.log_level + '" is incorrect.')

    @staticmethod
    def warning(text):
        logging.warning(text)
        if Logger.print_to_display_flag:
            Logger.__print_to_display_function(text, LogLevel.WARNING)

    @staticmethod
    def error(text):
        logging.error(text)
        if Logger.print_to_display_flag:
            Logger.__print_to_display_function(text, LogLevel.ERROR)

    @staticmethod
    def info(text):
        logging.info(text)
        if Logger.print_to_display_flag:
            Logger.__print_to_display_function(text, LogLevel.INFO)

    @staticmethod
    def __parse_log_level(log_level_string):
        for ll in LogLevel:
            if ll.name == log_level_string:
                return ll.name
        return LogLevel.INFO.value

    @staticmethod
    def __print_to_display_function(text, log_level):
        a = LogLevel[Logger.log_level].value
        b = log_level.value
        if LogLevel[Logger.log_level].value <= log_level.value:
            print(text)
