import time
from threading import Thread

from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.mumjolandia_mode import MumjolandiaMode
from src.modules.tasks.task_supervisor import TaskSupervisor


class MumjolandiaThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
        self.taskSupervisor = TaskSupervisor()
        self.mode = MumjolandiaMode.none

    def run(self):
        while True:
            command_string = self.__get_next_command()
            command = CommandFactory.get_command(command_string)
            if command.arguments[0] == 'task':
                arg_placeholder = command.arguments.pop(0)
                if self.taskSupervisor.execute(command):
                    command.arguments.insert(0, arg_placeholder)
                    print(command.arguments, '- Command not recognized :(')
                    continue
            elif command.arguments[0] == 'exit':
                print('mumjolandia exiting')
                break
            else:
                print('Unrecognized command: ')
                print(command.arguments, end=" ")

    def __get_next_command(self):
        command = self.queue.get()
        self.queue.task_done()
        return command
