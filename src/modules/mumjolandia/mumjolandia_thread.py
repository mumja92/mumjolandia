import copy
import logging
from threading import Thread
from src.interface.mumjolandia.mumjolandia_cli_mode import MumjolandiaCliMode
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.tasks.task_storage_type import StorageType
from src.modules.connection.connection_supervisor import ConnectionSupervisor
from src.modules.fat.fat_supervisor import FatSupervisor
from src.modules.food.food_supervisor import FoodSupervisor
from src.modules.game.game_supervisor import GameSupervisor
from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.note.note_supervisor import NoteSupervisor
from src.modules.tasks.task_supervisor import TaskSupervisor


class MumjolandiaThread(Thread):
    def __init__(self, queue_in, queue_response, event):
        Thread.__init__(self)
        self.config_object = ConfigLoader.get_config()
        self.queue_in = queue_in
        self.queue_response = queue_response
        self.supervisors = {}
        self.mode = MumjolandiaCliMode.none
        self.command_parsers = {}
        self.exit_flag = False
        self.command_done_event = event
        self.__init()

    def __del__(self):
        logging.info('mumjolandia thread exiting')

    def run(self):
        logging.info('mumjolandia thread started')
        while True:
            command = self.__get_next_command()
            command_to_pass = copy.copy(command)
            try:
                command_to_pass.arguments = command_to_pass.arguments[1:]
            except IndexError:
                command_to_pass.arguments = []
            try:
                return_value = self.command_parsers[command.arguments[0]](command_to_pass)
            except KeyError:
                logging.debug("Unrecognized command: '" + str(command) + "'")
                return_value = MumjolandiaResponseObject(status=MumjolandiaReturnValue.mumjolandia_unrecognized_command,
                                                         arguments=command)
            self.queue_response.put(return_value)
            self.command_done_event.set()
            if self.exit_flag:
                break

    def __init(self):
        try:
            self.supervisors['task'] = TaskSupervisor(storage_type=StorageType[self.config_object.task_io_method])
        except KeyError:
            logging.error('Storage type: "' + self.config_object.task_io_method + '" is incorrect. Using xml instead. ')
            self.supervisors['task'] = TaskSupervisor(storage_type=StorageType.xml)
        self.supervisors['food'] = FoodSupervisor('data/jedzonko.db')
        self.supervisors['fat'] = FatSupervisor('data/fat.pickle')
        self.supervisors['game'] = GameSupervisor('data/games.xml')
        self.supervisors['note'] = NoteSupervisor('data/notes.pickle')
        self.supervisors['connection'] = ConnectionSupervisor()

        self.command_parsers['exit'] = self.__command_exit
        self.command_parsers['task'] = self.__command_task
        self.command_parsers['food'] = self.__command_food
        self.command_parsers['fat'] = self.__command_fat
        self.command_parsers['game'] = self.__command_game
        self.command_parsers['note'] = self.__command_note
        self.command_parsers['connection'] = self.__command_connection
        self.command_parsers['ssh'] = self.__command_connection
        self.command_parsers['help'] = self.__command_help

    def __get_next_command(self):
        command = self.queue_in.get()
        self.queue_in.task_done()
        logging.debug("Parsing command: '" + str(command) + "'")
        return command

    def __command_exit(self, command):
        self.exit_flag = True
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.mumjolandia_exit)

    def __command_task(self, command):
        return self.supervisors['task'].execute(command)

    def __command_food(self, command):
        return self.supervisors['food'].execute(command)

    def __command_fat(self, command):
        return self.supervisors['fat'].execute(command)

    def __command_game(self, command):
        return self.supervisors['game'].execute(command)

    def __command_note(self, command):
        return self.supervisors['note'].execute(command)

    def __command_connection(self, command):
        return self.supervisors['connection'].execute(command)

    def __command_help(self, command):
        return_value = []
        for key, value in self.command_parsers.items():
            return_value.append(key)
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.mumjolandia_help,
                                         arguments=return_value)
