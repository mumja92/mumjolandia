from pathlib import Path

from src.interface.mumjolandia.mumjolandia_config_object import MumjolandiaConfigObject
from src.interface.mumjolandia.mumjolandia_config_enums import MumjolandiaLogLevel, MumjolandiaConfigBool
from src.interface.tasks.task_storage_type import TaskStorageType
from src.external.xmltodict import xmltodict


class ConfigLoader:
    @staticmethod
    def get_config():
        config_location = 'data/config.xml'
        file = Path(config_location)
        config_values = {'log_level': 'WARNING',
                         'log_to_display': 'True',
                         'log_to_file': 'False',
                         'task_io_method': 'xml'}
        config_enums = {'log_level': MumjolandiaLogLevel,
                        'log_to_display': MumjolandiaConfigBool,
                        'log_to_file': MumjolandiaConfigBool,
                        'task_io_method': TaskStorageType}
        if file.is_file():
            with open(config_location, 'r') as my_file:
                data = my_file.read()
            config_dict = xmltodict.parse(data)
            for key, value in config_values.items():
                try:
                    value_to_check = config_dict['config'][key]
                    if ConfigLoader.__is_value_in_enum(value_to_check, config_enums[key]):
                        config_values[key] = value_to_check

                except KeyError:
                    pass
        return MumjolandiaConfigObject(**config_values)

    @staticmethod
    def __is_value_in_enum(value, enum):
        for i in enum:
            if value.upper() == i.name.upper():
                return True
        return False
