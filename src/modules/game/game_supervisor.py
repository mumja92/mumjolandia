import logging

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.game.game_db_adapter import GameDbAdapter
from src.modules.game.game_factory import GameFactory
from src.utils.shared_preferences import SharedPreferences


class GameSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location='data/games.db'):
        super().__init__()
        self.game_file_location = file_location
        self.games_loader = GameDbAdapter(self.game_file_location)
        self.games = None
        self.current_game_id = SharedPreferences().get('current_game_id')
        self.__init()

    def __init(self):
        self.__add_command_parsers()
        self.games = self.games_loader.get_games()

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['current'] = self.__command_current
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['remove'] = self.__command_remove
        self.command_parsers['set'] = self.__command_set

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

    def __command_current(self, args):
        if self.current_game_id is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_current_get, arguments=[None])
        else:
            for g in self.games:
                if g.game_id == self.current_game_id:
                    return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_current_get, arguments=[g.name])
            logging.error("Didn't found game with current_game_id!")
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_current_get, arguments=[None])

    def __command_get(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_get_ok, arguments=self.games)

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_help,
                                         arguments=['current\n'
                                                    'ls\n'
                                                    'add [name]\n'
                                                    'remove [name]\n'
                                                    'set [id/name]\n'
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

    def __command_set(self, args):
        if args is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_set_wrong_id, arguments=[])
        found_game_id = None
        try:
            arg_as_int = int(args[0])
        except ValueError:
            arg_as_int = None
        if arg_as_int is not None:
            for g in self.games:
                if arg_as_int == g.game_id:
                    found_game_id = g.game_id
                    break
        else:
            for g in self.games:
                if args[0] == g.name:
                    found_game_id = g.game_id
                    break
        if found_game_id is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_set_wrong_id, arguments=[])
        else:
            SharedPreferences().put('current_game_id', found_game_id)
            self.current_game_id = found_game_id
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_set_ok, arguments=[])
