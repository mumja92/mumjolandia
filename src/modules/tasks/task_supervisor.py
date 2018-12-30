import datetime
import logging

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.interface.tasks.task_file_broken_exception import TaskFileBrokenException
from src.interface.mumjolandia.incorrect_date_format_exception import IncorrectDateFormatException
from src.interface.tasks.task_storage_type import StorageType
from src.modules.tasks.task_factory import TaskFactory
from src.utils.object_loader_pickle import ObjectLoaderPickle
from src.modules.tasks.task_loader_xml import TaskLoaderXml


class TaskSupervisor(MumjolandiaSupervisor):
    def __init__(self, storage_type=StorageType.xml):
        super().__init__()
        self.storage_type = storage_type
        self.task_file_location = "data/tasks." + self.storage_type.name
        self.allowedToSaveTasks = True  # if loaded tasks are broken they wont be overwritten to not loose them
        self.task_loader = None
        self.tasks = None
        self.__init()

    def get_tasks(self):
        return self.tasks

    def add_task(self, name):
        try:
            self.tasks.append(TaskFactory.get_task(name))
        except IncorrectDateFormatException:
            logging.warning("Task '" + name + "' not added - incorrect date format")
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_incorrect_date_format)
        logging.info("Added task '" + name + "'")
        self.__save_if_allowed()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_added, arguments=[name])

    def edit_task(self, task_id, new_task):
        try:
            self.tasks[task_id] = new_task
            self.__save_if_allowed()
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_edit_ok,
                                             arguments=[str(task_id)])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_edit_wrong_index,
                                             arguments=[str(task_id)])

    def delete_task(self, task_id):
        # parameter comes as string. If we can parse it to int then we remove by id. If not, then by name
        try:
            tid = int(task_id)
            try:
                self.tasks.pop(tid)
                self.__save_if_allowed()
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
                self.__save_if_allowed()
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_delete_success,
                                                 arguments=[task_id, str(deleted_counter)])

    def __init(self):
        self.__add_command_parsers()

        if self.storage_type == StorageType.xml:
            self.task_loader = TaskLoaderXml(self.task_file_location)
        elif self.storage_type == StorageType.pickle:
            self.task_loader = ObjectLoaderPickle(self.task_file_location)
        else:
            logging.error("Unrecognized storage type: '" + str(self.storage_type.name) + "' - using xml instead")
            self.task_loader = TaskLoaderXml(self.task_file_location)

        try:
            self.tasks = self.task_loader.get()
        except FileNotFoundError:
            logging.info(self.task_file_location + " - file doesn't exist")
            self.tasks = []
        except TaskFileBrokenException as e:
            print('Task file broken. Not saving changes!')
            logging.error(self.task_file_location + ' - file broken. Not saving changes!')
            self.tasks = e.args[0]
            self.allowedToSaveTasks = False

    def __save_if_allowed(self):
        if self.allowedToSaveTasks:
            logging.debug("saving tasks to: '" + self.task_file_location + "'")
            self.task_loader.save(self.tasks)

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['delete'] = self.__command_delete
        self.command_parsers['edit'] = self.__command_edit
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['set'] = self.__command_set

    def __command_add(self, args):
        if len(args) < 1:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_name_not_given)
        else:
            return self.add_task(' '.join(args[0:]))

    def __command_get(self, args):  # 'get' - return today, 'get 1' - return tomorrow,get '0' - return all
        return_list = []
        return_status = MumjolandiaReturnValue.task_get
        if args:
            try:
                day_amount = int(args[0])
            except ValueError:
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_get_wrong_data, arguments=args)
            if int(args[0]) == 0:
                return_list = self.tasks
            else:
                for t in self.tasks:
                    temp = datetime.datetime.combine(datetime.datetime.today() + datetime.timedelta(days=day_amount),
                                                     datetime.datetime.min.time())
                    if t.date_to_finish.year == temp.year and \
                            t.date_to_finish.month == temp.month and \
                            t.date_to_finish.day == temp.day:
                        return_list.append(t)
        else:
            for t in self.tasks:
                temp = datetime.datetime.today()
                if t.date_to_finish.year == temp.year and \
                        t.date_to_finish.month == temp.month and \
                        t.date_to_finish.day == temp.day:
                    return_list.append(t)
        return MumjolandiaResponseObject(status=return_status, arguments=return_list)

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_help,
                                         arguments=['print, add [name], delete [name || id], edit [id] [name]'])

    def __command_delete(self, args):
        try:
            return self.delete_task(args[0])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_delete_incorrect_index,
                                             arguments=['none'])

    def __command_edit(self, args):
        return self.edit_task(int(args[0]), TaskFactory.get_task(name=args[1]))

    def __command_set(self, args):
        try:
            if int(args[0]) > len(self.tasks) or int(args[0]) < 0:
                raise IndexError
            self.tasks[int(args[0])].date_to_finish = datetime.datetime.today().replace(microsecond=0) + \
                                                      datetime.timedelta(days=int(args[1]))
            self.__save_if_allowed()
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_set_ok,
                                             arguments=[self.tasks[int(args[0])].name, args[1]])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_set_incorrect_parameter,
                                             arguments=args)
