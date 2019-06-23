import logging

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.game.game_loader import GameLoader


class GameSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location):
        super().__init__()
        self.game_file_location = file_location
        self.games_loader = GameLoader(self.game_file_location)
        self.games = None
        self.__init()

    def __init(self):
        self.__add_command_parsers()
        self.games = self.games_loader.get()

    def __add_command_parsers(self):
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help

    def __command_get(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_get_ok, arguments=self.games)

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_help,
                                         arguments=['print'])
