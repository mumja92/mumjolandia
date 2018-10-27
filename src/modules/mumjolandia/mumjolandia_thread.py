import copy
import logging
import sys
from threading import Thread
from src.interface.mumjolandia.mumjolandia_mode import MumjolandiaMode


class MumjolandiaThread(Thread):
    def __init__(self, queue, supervisors):
        Thread.__init__(self)
        self.queue = queue
        self.supervisors = supervisors
        self.taskSupervisor = self.supervisors['task']
        self.mode = MumjolandiaMode.none
        self.command_parsers = {}
        self.exit_flag = False
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
                self.command_parsers[command.arguments[0]](command_to_pass)
            except KeyError:
                print('Unrecognized command: ', command.arguments, sep=' ', end='\n', file=sys.stdout, flush=False)
            if self.exit_flag:
                break

    def __init(self):
        self.command_parsers['exit'] = self.__command_exit
        self.command_parsers['task'] = self.__command_task

    def __get_next_command(self):
        command = self.queue.get()
        self.queue.task_done()
        return command

    def __command_exit(self, command):
        self.exit_flag = True
        logging.info('mumjolandia thread exiting')

    def __command_task(self, command):
        self.supervisors['task'].execute(command)
