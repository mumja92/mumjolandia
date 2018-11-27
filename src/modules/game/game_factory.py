from src.interface.game.game import Game


class GameFactory:
    @staticmethod
    def get_game(name, description='-'):
        return Game(str(name), str(description))
