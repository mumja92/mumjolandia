import logging
import socket

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
import http.client
import json


class WeatherSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help

    def __command_get(self, args):
        response = self.__get_weather_now()
        if response is not None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.weather_get_ok,
                                             arguments=[response])
        else:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.weather_get_nook,
                                             arguments=['Connection failed'])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.weather_help,
                                         arguments=['get'])

    def __get_weather_now(self):
        try:
            connection = http.client.HTTPConnection("fcc-weather-api.glitch.me")
            connection.request("GET", "/api/current?lat=51.1&lon=17.03")
            response = connection.getresponse()
        except socket.gaierror:
            logging.warning('Could not connect to service')
            return None
        return_value = None
        if response.status == 200:
            json_response = json.loads(response.read().decode())
            weather = json_response['weather'][0]['main']
            temperature = json_response['main']['temp']
            return_value = weather + ' ' + '%.1f' % temperature + 'C'
        else:
            logging.warning('Weather API returned non 200-response')
        connection.close()
        return return_value
