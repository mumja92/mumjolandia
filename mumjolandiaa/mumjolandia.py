#!/usr/bin/env python
from mumjolandiaa.console.console import Console
from mumjolandiaa.mumjolandia_mode import MumjolandiaMode
from mumjolandiaa.views.tasks.task_supervisor import TaskSupervisor

class Mumjolandia:
    def __init__(self):
        self.console = Console()
        self.taskSupervisor = TaskSupervisor()
        self.mode = MumjolandiaMode.none

    def run(self):
        while True:
            print(' ')
            command = self.console.get_next_command()
            if command.arguments[0] == 'task':
                arg_placeholder = command.arguments.pop(0)
                if self.taskSupervisor.execute(command):
                    command.arguments.insert(0, arg_placeholder)
                    print(command.arguments, '- Command not recognized :(')
                    continue
            elif command.arguments[0] == 'exit':
                break
            else:
                print('Unrecognized command: ')
                print(command.arguments, end=" ")
