import copy
import logging
from threading import Thread
from src.interface.mumjolandia.mumjolandia_mode import MumjolandiaMode
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue


class MumjolandiaThread(Thread):
    def __init__(self, queue_in, queue_response, supervisors, event):
        Thread.__init__(self)
        self.queue_in = queue_in
        self.queue_response = queue_response
        self.supervisors = supervisors
        self.mode = MumjolandiaMode.none
        self.command_parsers = {}
        self.exit_flag = False
        self.command_done_event = event
        self.__init()

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
                return_value = MumjolandiaResponseObject(status=MumjolandiaReturnValue.unrecognized_command)
            self.queue_response.put(return_value)
            self.command_done_event.set()
            if self.exit_flag:
                break

    def __init(self):
        self.command_parsers['exit'] = self.__command_exit
        self.command_parsers['task'] = self.__command_task

    def __get_next_command(self):
        command = self.queue_in.get()
        self.queue_in.task_done()
        logging.debug("Parsing command: '" + str(command) + "'")
        return command

    def __command_exit(self, command):
        self.exit_flag = True
        logging.info('mumjolandia thread exiting')
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.exit)

    def __command_task(self, command):
        return self.supervisors['task'].execute(command)
