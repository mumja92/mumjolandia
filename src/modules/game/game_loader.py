from pathlib import Path
from src.interface.game.game_type import GameType
from src.interface.game.games_container import GamesContainer
from src.external.xmltodict import xmltodict
from src.modules.game.game_factory import GameFactory


class GameLoader:
    def __init__(self, filename):
        self.file = filename

    def get(self):
        games = GamesContainer()
        file = Path(self.file)
        if not file.is_file():
            return games
        with open(self.file, 'r') as my_file:
            data = my_file.read()
        d = xmltodict.parse(data)
        for game_type in GameType:
            if isinstance(d['games'][game_type.name], type(None)):              # node empty
                continue
            elif isinstance(d['games'][game_type.name]['game'], str):           # node has 1 element
                games.add(str(d['games'][game_type.name]['game']), game_type)
            elif isinstance(d['games'][game_type.name]['game'], list):          # node has many elements
                for g in d['games'][game_type.name]['game']:
                    games.add(GameFactory().get_game(name=g, description='', game_type=game_type), game_type)
        return games

    def save(self):
        pass
