import logging

from src.interface.tasks.task_file_broken_exception import TaskFileBrokenException
from src.interface.tasks.task_priority import TaskPriority
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_loader_xml import TaskLoader


class TaskSupervisor:
    def __init__(self):
        self.allowedToSaveTasks = True           # if loaded tasks are broken they wont be overwritten to not loose them
        self.task_loader = TaskLoader("tasks.xml")
        try:
            self.tasks = self.task_loader.get_tasks()
        except FileNotFoundError:
            logging.info('TaskSupervisor::constructor - file doesnt exist')
            self.tasks = []
        except TaskFileBrokenException as e:
            print('Task file broken. Not saving changes!')
            logging.error('TaskSupervisor::constructor - file broken. Not saving changes!')
            self.tasks = e.args[0]
            self.allowedToSaveTasks = False

    def __del__(self):
        if self.allowedToSaveTasks:
            self.task_loader.save_tasks(self.tasks)

    def print(self):
        print(len(self.tasks), 'items:')
        for t in self.tasks:
            print(t.text, t.date, t.priority)

    def add_task(self, name):
        self.tasks.append(TaskFactory.get_task(name, TaskPriority.ez))
        return 0

    def execute(self, command):
        command_length = len(command.arguments)
        if command_length == 0:
            print('Commands:')
            print('print, add x')
            return 0
        if command.arguments[0] == 'print':
            self.print()
            return 0
        elif command.arguments[0] == 'add':
            if command_length < 2:
                print('Task name not given')
                return 0
            else:
                task_name = ' '.join(command.arguments[1:])  #concat every arg but first into one
                if not self.add_task(task_name):
                    print('ok')
                    return 0
                return 1
        else:
            return 1
