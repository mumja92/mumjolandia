import logging

from src.interface.mumjolandia.mumjolandia_config_object import MumjolandiaConfigObject
from src.utils import xmltodict


class ConfigLoader:
    @staticmethod
    def get_config_starter():
        with open('data/config.xml', 'r') as my_file:
            data = my_file.read()
        config_dict = xmltodict.parse(data)
        return MumjolandiaConfigObject(config_dict['config']['log_level'],
                                       config_dict['config']['task_io_method'])
