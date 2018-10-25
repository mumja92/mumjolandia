import logging

from src.interface.tasks.task_file_broken_exception import TaskFileBrokenException
from src.interface.tasks.task_priority import TaskPriority
from src.interface.tasks.task_storage_type import StorageType
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_loader_pickle import TaskLoaderPickle
from src.modules.tasks.task_loader_xml import TaskLoaderXml


class TaskSupervisor:
    def __init__(self, storage_type=StorageType.xml):
        self.storage_type = storage_type
        self.task_file_location = "data/tasks." + self.storage_type.name
        self.allowedToSaveTasks = True           # if loaded tasks are broken they wont be overwritten to not loose them
        self.task_loader = TaskLoaderXml(self.task_file_location)
        if storage_type == StorageType.xml:
            self.task_loader = TaskLoaderXml(self.task_file_location)
        elif storage_type == StorageType.pickle:
            self.task_loader = TaskLoaderPickle(self.task_file_location)
        else:
            logging.error("Unrecognized storage type: '" + self.storage_type + "' - using xml instead")
        try:
            self.tasks = self.task_loader.get_tasks()
        except FileNotFoundError:
            logging.info(self.task_file_location + " - file doesn't exist")
            self.tasks = []
        except TaskFileBrokenException as e:
            print('Task file broken. Not saving changes!')
            logging.error(self.task_file_location + ' - file broken. Not saving changes!')
            self.tasks = e.args[0]
            self.allowedToSaveTasks = False

    def __del__(self):
        if self.allowedToSaveTasks:
            logging.debug("saving tasks to: '" + self.task_file_location + "'")
            self.task_loader.save_tasks(self.tasks)
        else:
            logging.debug("Not saving tasks")

    def print(self):
        print(len(self.tasks), 'items:')
        for t in self.tasks:
            print(str(t))

    def add_task(self, name):
        logging.info("Adding task '" + name + "'")
        self.tasks.append(TaskFactory.get_task(name))
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
