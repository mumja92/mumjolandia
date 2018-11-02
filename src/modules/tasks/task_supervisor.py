import logging

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.tasks.task_file_broken_exception import TaskFileBrokenException
from src.interface.tasks.task_incorrect_date_format_exception import TaskIncorrectDateFormatException
from src.interface.tasks.task_storage_type import StorageType
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_loader_pickle import TaskLoaderPickle
from src.modules.tasks.task_loader_xml import TaskLoaderXml


class TaskSupervisor:
    def __init__(self, storage_type=StorageType.xml):
        self.storage_type = storage_type
        self.task_file_location = "data/tasks." + self.storage_type.name
        self.allowedToSaveTasks = True           # if loaded tasks are broken they wont be overwritten to not loose them
        self.task_loader = None
        self.tasks = None
        self.command_parsers = {}
        self.__init()

    def __del__(self):
        if self.allowedToSaveTasks:
            logging.debug("saving tasks to: '" + self.task_file_location + "'")
            self.task_loader.save_tasks(self.tasks)
        else:
            logging.debug("Not saving tasks")

    def get_tasks(self):
        return self.tasks

    def add_task(self, name):
        try:
            self.tasks.append(TaskFactory.get_task(name))
        except TaskIncorrectDateFormatException:
            logging.warning("Task '" + name + "' not added - incorrect date format")
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_incorrect_date_format)
        logging.info("Added task '" + name + "'")
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_added, arguments=[name])

    def delete_task(self, task_id):
        # parameter comes as string. If we can parse it to int then we remove by id. If not, then by name
        try:
            tid = int(task_id)
            try:
                self.tasks.pop(tid)
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_delete_success,
                                                 arguments=[task_id, str(1)])
            except IndexError:  # wrong index
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_delete_incorrect_index,
                                                 arguments=[task_id])
        except ValueError:  # parameter type is not int
            deleted_counter = 0
            for t in reversed(self.tasks):  # reversing allows to remove elements on fly without breaking ids
                if t.name == task_id:
                    self.tasks.remove(t)
                    deleted_counter += 1
            if deleted_counter == 0:
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_delete_incorrect_name,
                                                 arguments=[task_id])
            else:
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_delete_success,
                                                 arguments=[task_id, str(deleted_counter)])

    def execute(self, command):

        try:
            return self.command_parsers[command.arguments[0]](command.arguments[1:])
        except KeyError:
            logging.warning('Unrecognized command: ' + str(command.arguments))
            return self.command_parsers['unrecognized_command'](command.arguments)
        except IndexError:
            return self.command_parsers['null'](command.arguments)

    def __init(self):
        self.__add_command_parsers()

        if self.storage_type == StorageType.xml:
            self.task_loader = TaskLoaderXml(self.task_file_location)
        elif self.storage_type == StorageType.pickle:
            self.task_loader = TaskLoaderPickle(self.task_file_location)
        else:
            logging.error("Unrecognized storage type: '" + str(self.storage_type.name) + "' - using xml instead")
            self.task_loader = TaskLoaderXml(self.task_file_location)

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

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['null'] = self.__command_null
        self.command_parsers['print'] = self.__command_print
        self.command_parsers['unrecognized_command'] = self.__unrecognized_command
        self.command_parsers['delete'] = self.__command_delete

    def __command_add(self, args):
        if len(args) < 1:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_name_not_given)
        else:
            return self.add_task(args[0])

    def __command_null(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_null)

    def __command_print(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_print, arguments=self.tasks)

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_help, arguments=['print, add x'])

    def __unrecognized_command(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_unrecognized_parameters, arguments=args)

    def __command_delete(self, args):
        return self.delete_task(args[0])
