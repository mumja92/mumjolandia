import logging

from src.interface.game.game import Game


class GameFactory:
    @staticmethod
    def get_game(name, game_id):
        if not isinstance(name, str):
            logging.warning('game name incorrect')
            return None
        if not isinstance(game_id, int):
            logging.warning('game id must be int')
            return None
        return Game(name, game_id)
