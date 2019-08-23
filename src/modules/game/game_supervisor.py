from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.game.game_db_adapter import GameDbAdapter
from src.modules.game.game_factory import GameFactory


class GameSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location='data/games.db'):
        super().__init__()
        self.game_file_location = file_location
        self.games_loader = GameDbAdapter(self.game_file_location)
        self.games = None
        self.__init()

    def __init(self):
        self.__add_command_parsers()
        self.games = self.games_loader.get_games()

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['remove'] = self.__command_remove

    def __command_add(self, args):
        try:
            game = GameFactory().get_game(' '.join(args[0:]), -1)
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_value_not_given, arguments=[])
        for g in self.games:
            if game.name.lower() == g.name.lower():     # Treat games with same name but different captions as the same
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_exist, arguments=[game.name])
        if self.games_loader.add_game(game):
            self.games = self.games_loader.get_games()
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_added, arguments=[game.name])
        else:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_exist, arguments=[game.name])

    def __command_get(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_get_ok, arguments=self.games)

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_help,
                                         arguments=['ls\n'
                                                    'add [name]\n'
                                                    'remove [name]\n'
                                                    'help'])

    def __command_remove(self, args):
        try:
            game_name = ' '.join(args[0:])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_delete_incorrect_index, arguments=[])
        game = None
        for g in self.games:
            if g.name.lower() == game_name.lower():
                game = g
        if game is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_delete_incorrect_index, arguments=[])
        else:
            removed_count = self.games_loader.remove_game(game)
            self.games = self.games_loader.get_games()
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_delete_success,
                                             arguments=[removed_count, game_name])
