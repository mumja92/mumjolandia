import logging

from src.interface.game.game import Game
from src.interface.game.game_type import GameType


class GameFactory:
    @staticmethod
    def get_game(name, game_type, description=''):
        if not isinstance(game_type, GameType):
            logging.warning('game_type incorrect')
            return None
        if not isinstance(name, str):
            logging.warning('game name incorrect')
            return None
        if not isinstance(description, str):
            logging.warning('game description incorrect')
            description = ''
        return Game(name, game_type, description)
