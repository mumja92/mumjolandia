import logging

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.game.game_factory import GameFactory
from src.utils.object_loader_pickle import ObjectLoaderPickle


class GameSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location):
        super().__init__()
        self.game_file_location = file_location
        self.games_loader = ObjectLoaderPickle(self.game_file_location)
        self.games = []
        self.__init()

    def get_games(self):
        return self.games

    def add_game(self, name, desc):
        self.games.append(GameFactory.get_game(name, desc))
        self.__save()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_added, arguments=[name])

    def delete_game(self, game_id):
        # parameter comes as string. If we can parse it to int then we remove by id. If not, then by name
        try:
            gid = int(game_id)
            try:
                self.games.pop(gid)
                self.__save()
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_delete_success,
                                                 arguments=[game_id, str(1)])
            except IndexError:  # wrong index
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_delete_incorrect_index,
                                                 arguments=[game_id])
        except ValueError:  # parameter type is not int
            deleted_counter = 0
            for g in reversed(self.games):  # reversing allows to remove elements on fly without breaking ids
                if g.name == game_id:
                    self.games.remove(g)
                    deleted_counter += 1
            if deleted_counter == 0:
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_delete_incorrect_name,
                                                 arguments=[game_id])
            else:
                self.__save()
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_delete_success,
                                                 arguments=[game_id, str(deleted_counter)])

    def __init(self):
        self.__add_command_parsers()
        self.games = self.games_loader.get()

    def __save(self):
        logging.debug("saving games to: '" + self.game_file_location + "'")
        self.games_loader.save(self.games)

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['delete'] = self.__command_delete
        self.command_parsers['help'] = self.__command_help

    def __command_add(self, args):
        if len(args) < 2:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_value_not_given)
        else:
            return self.add_game(args[0], ' '.join(args[1:]))

    def __command_get(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_get_ok, arguments=self.games)

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_help,
                                         arguments=['print, add [name] [description], delete [name || id]'])

    def __command_delete(self, args):
        try:
            return self.delete_game(args[0])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_delete_incorrect_index,
                                             arguments=['none'])
