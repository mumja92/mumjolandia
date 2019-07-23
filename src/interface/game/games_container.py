from src.interface.game.game_type import GameType
from src.interface.game.wrong_game_type_exception import WrongGameTypeException


class GamesContainer:
    def __init__(self):
        self.games = {}
        for game_type in GameType:
            self.games[game_type.name] = []

    def add(self, game_name, game_type):
        if isinstance(game_type, GameType):
            if game_name not in self.games[game_type.name]:
                self.games[game_type.name].append(game_name)
        else:
            raise WrongGameTypeException()

    def __str__(self):
        pre_game_string = '   '
        return_string = ''
        for game_type in GameType:
            return_string += game_type.name + '\n'
            for game in self.games[game_type.name]:
                return_string += pre_game_string + str(game) + '\n'
        return return_string
