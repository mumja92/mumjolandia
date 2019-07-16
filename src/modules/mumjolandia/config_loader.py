import ipaddress
import logging
import xml
from enum import Enum
from pathlib import Path

from src.interface.mumjolandia.mumjolandia_config_object import MumjolandiaConfigObject
from src.interface.mumjolandia.mumjolandia_config_enums import MumjolandiaLogLevel, MumjolandiaConfigBool
from src.interface.tasks.task_storage_type import TaskStorageType
from src.external.xmltodict import xmltodict


class ConfigLoader:
    @staticmethod
    def get_config(config_location='data/config.xml'):
        file = Path(config_location)
        config_values = {'log_level': 'WARNING',
                         'log_to_display': 'True',
                         'log_to_file': 'False',
                         'task_io_method': 'xml',
                         'server_address': '127.0.0.1',
                         'server_port': '3333'}
        config_enums = {'log_level': MumjolandiaLogLevel,
                        'log_to_display': MumjolandiaConfigBool,
                        'log_to_file': MumjolandiaConfigBool,
                        'task_io_method': TaskStorageType,
                        'server_address': 'ip',
                        'server_port': 'port'}
        if file.is_file():
            with open(config_location, 'r') as my_file:
                data = my_file.read()
            try:
                config_dict = xmltodict.parse(data)
            except xml.parsers.expat.ExpatError as e:
                config_dict = None
            for key, value in config_values.items():
                try:
                    value_to_check = config_dict['config'][key]
                    if ConfigLoader.__is_value_correct(value_to_check, config_enums[key]):
                        config_values[key] = value_to_check

                except KeyError:
                    logging.warning('KeyError for key: ' + str(key))
                    pass
                except TypeError:       # value does not exist
                    logging.warning('TypeError for key: ' + str(key))
                    pass
                except AttributeError:  # value is empty
                    pass
        return MumjolandiaConfigObject(**config_values)

    @staticmethod
    def __is_value_correct(value, parameter):
        if isinstance(parameter, str):
            if parameter == 'ip':
                try:
                    ipaddress.ip_address(value)
                except ValueError:
                    logging.warning('Incorrect server ip address format')
                    return False
                return True
            if parameter == 'port':
                try:
                    number = int(value)
                    if number < 1024 or number > 65535:
                        logging.warning('Server port out of required bounds[1024-65535]')
                        return False
                    return True
                except ValueError:
                    logging.warning('Incorrect server port format')
                    return False
        elif issubclass(parameter, Enum):
            return ConfigLoader.__is_value_in_enum(value, parameter)
        else:
            return False

    @staticmethod
    def __is_value_in_enum(value, enum):
        for i in enum:
            if value.upper() == i.name.upper():
                return True
        return False
