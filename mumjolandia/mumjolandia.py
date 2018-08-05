#!/usr/bin/env python
from mumjolandia.console.console import Console
from mumjolandia.mumjolandia_mode import MumjolandiaMode
from mumjolandia.tasks.task_supervisor import TaskSupervisor


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
                passed = command
                passed.arguments.pop(0)
                if self.taskSupervisor.execute(passed):
                    print('Command not recognized :(')
                    continue
            elif command.arguments[0] == 'exit':
                break
            else:
                print('Unrecognized command: ')
                print(command.arguments, end=" ")
