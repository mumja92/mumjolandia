import datetime
import logging

from src.modules.tasks.periodic.periodic_task_generator import PeriodicTaskGenerator

from src.interface.mumjolandia.incorrect_date_format_exception import IncorrectDateFormatException
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.tasks.task_file_broken_exception import TaskFileBrokenException
from src.interface.tasks.task_status import TaskStatus
from src.interface.tasks.task_storage_type import TaskStorageType
from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.tasks.periodic.periodic_task_progress_handler import PeriodicTaskProgressHandler
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_loader_xml import TaskLoaderXml
from src.utils.object_loader_pickle import ObjectLoaderPickle


class TaskSupervisor(MumjolandiaSupervisor):
    def __init__(self, storage_type=TaskStorageType.xml):
        super().__init__()
        self.storage_type = storage_type
        self.periodic_tasks_location = ConfigLoader.get_mumjolandia_location() + "data/periodic_tasks.xml"
        self.task_file_location = ConfigLoader.get_mumjolandia_location() + "data/tasks." + self.storage_type.name.lower()
        self.allowedToSaveTasks = True  # if loaded tasks are broken they wont be overwritten to not loose them
        self.task_loader = None
        self.tasks = None
        self.__init()

    def __init(self):
        self.__add_command_parsers()

        if self.storage_type == TaskStorageType.xml:
            logging.info("using xml file: " + self.task_file_location)
            self.task_loader = TaskLoaderXml(self.task_file_location)
        elif self.storage_type == TaskStorageType.pickle:
            logging.info("using pickle file: " + self.task_file_location)
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

    def __get_today(self):
        return datetime.datetime.today()

    def __save_if_allowed(self):
        if self.allowedToSaveTasks:
            logging.debug("saving tasks to: '" + self.task_file_location + "'")
            self.task_loader.save(self.tasks)

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['bump'] = self.__command_bump
        self.command_parsers['b'] = self.__command_bump
        self.command_parsers['done'] = self.__command_done
        self.command_parsers['edit'] = self.__command_edit
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['ls'] = self.__command_get
        self.command_parsers['periodic'] = self.__command_periodic
        self.command_parsers['rm'] = self.__command_delete
        self.command_parsers['set'] = self.__command_set
        self.command_parsers['undone'] = self.__command_undone

    def __command_add(self, args):
        if len(args) < 1:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_name_not_given)
        else:
            name = ' '.join(args[0:])
            try:
                self.tasks.append(TaskFactory.get_task(name))
            except IncorrectDateFormatException:
                logging.warning("Task '" + name + "' not added - incorrect date format")
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_incorrect_date_format)
            logging.info("Added task '" + name + "'")
            self.__save_if_allowed()
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_added,
                                             arguments=[name, len(self.tasks) - 1])

    def __command_get(self, args):  # 'get' - return today, 'get 1' - return tomorrow,get '0' - return all
        return_list = []
        return_indexes = []
        return_status = MumjolandiaReturnValue.task_get
        day_amount = 0
        if args:
            try:
                day_amount = int(args[0])
            except ValueError:
                if args[0] != 'x':
                    return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_get_wrong_data, arguments=args)
            if args[0] == 'x':   # task get x  ### every task that has finish date not set
                for i, t in enumerate(self.tasks):
                    if t.date_to_finish is None:
                        if t.status is not TaskStatus.done:
                            return_list.append(t)
                            return_indexes.append(i)
            elif int(args[0]) == 0:   # task get 0
                for i, t in enumerate(self.tasks):
                    return_list.append(t)
                    return_indexes.append(i)

            else:                   # task get [number]
                for i, t in enumerate(self.tasks):
                    temp = datetime.datetime.combine(self.__get_today() + datetime.timedelta(days=day_amount),
                                                     datetime.datetime.min.time())
                    if t.date_to_finish is not None:
                        if t.date_to_finish.year == temp.year and \
                                t.date_to_finish.month == temp.month and \
                                t.date_to_finish.day == temp.day:
                            return_list.append(t)
                            return_indexes.append(i)
        else:       # task get
            for i, t in enumerate(self.tasks):
                temp = self.__get_today()    # first tasks for today
                if t.date_to_finish is not None and t.status is not TaskStatus.done:
                    if (t.date_to_finish - temp).days * 24 + (t.date_to_finish - temp).seconds // 3600 <= t.reminder*24:
                        return_list.append(t)
                        return_indexes.append(i)
                        continue
                    # now not finished tasks from previous days
                    if t.status == TaskStatus.not_done and t.date_to_finish <= temp:
                        return_list.append(t)
                        return_indexes.append(i)
                # tasks from previous days and finished today
                if t.date_finished is not None:
                    if t.status == TaskStatus.done:
                        if t.date_finished.year == temp.year and \
                                t.date_finished.month == temp.month and \
                                t.date_finished.day == temp.day:
                            return_list.append(t)
                            return_indexes.append(i)
            try:
                return_indexes, return_list = zip(*self.__sort_ls(list(zip(return_indexes, return_list))))
                # zip returned tuples
                return_list = list(return_list)
                return_indexes = list(return_indexes)
            except ValueError:
                # it occurs when lists are empty: ValueError: not enough values to unpack (expected 2, got 0)
                pass
        if args and args[0] == 'x':
            return MumjolandiaResponseObject(status=return_status, arguments=[return_indexes, return_list])
        tasks = PeriodicTaskGenerator(self.periodic_tasks_location).get_tasks(day_amount)
        for n, t in enumerate(tasks):
            if PeriodicTaskProgressHandler(self.periodic_tasks_location).is_done(
                    self.__translate_periodic_task_id(self.__translate_periodic_task_id(n))):
                t.status = TaskStatus.done
            else:
                t.status = TaskStatus.not_done
            return_list.insert(0, t)
            return_indexes.insert(0, self.__translate_periodic_task_id(n))
        return MumjolandiaResponseObject(status=return_status, arguments=[return_indexes, return_list])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_help,
                                         arguments=['add [name]\n'
                                                    '[b]ump\n'
                                                    'done\n'
                                                    'edit [id] [name]\n'
                                                    'ls (show today and previous uncompleted\n'
                                                    'ls 0 (show all tasks\n'
                                                    'ls x (show tasks without date)\n'
                                                    'ls [delta] (show tasks for given day)\n'
                                                    'ls [name || id]\n'
                                                    'periodic\n'
                                                    'set [id] [delta_from_today/none]\n'
                                                    'undone\n'
                                                    ])

    def __command_delete(self, args):
        try:
            task_id = args[0]
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_delete_incorrect_index,
                                             arguments=['none'])
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

    def __command_edit(self, args):
        try:
            task_id = int(args[0])
        except IndexError:  # first argument not given
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_edit_wrong_index,
                                             arguments=['None'])
        try:
            if len(args) < 2:
                raise IndexError
            new_task = TaskFactory.get_task(name=' '.join(args[1:]), date_to_finish=self.tasks[int(args[0])].date_to_finish)
            self.tasks[task_id] = new_task
            self.__save_if_allowed()
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_edit_ok,
                                             arguments=[str(task_id)])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_edit_wrong_index,
                                             arguments=[str(task_id)])

    def __command_set(self, args):
        try:
            if int(args[0]) > len(self.tasks) or int(args[0]) < 0:
                raise IndexError
            # parsing first argument
            if args[1].lower() == 'None'.lower():
                self.tasks[int(args[0])].date_to_finish = None
            else:
                self.tasks[int(args[0])].date_to_finish = self.__get_today().replace(microsecond=0) + \
                                                          datetime.timedelta(days=int(args[1]))
            # parsing second argument
            if len(args) > 2:
                self.tasks[int(args[0])].reminder = int(args[2])
            self.__save_if_allowed()
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_set_ok,
                                             arguments=[self.tasks[int(args[0])].name, args[1]])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_set_incorrect_parameter,
                                             arguments=args)
        except ValueError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_set_incorrect_parameter,
                                             arguments=args)

    def __command_done(self, args):
        try:
            if int(args[0]) > len(self.tasks):
                raise IndexError
            if int(args[0]) < 0:
                return_value = PeriodicTaskProgressHandler(self.periodic_tasks_location).set_done(
                    self.__translate_periodic_task_id(int(args[0])))
                if return_value is not True:
                    return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_done_wrong_parameter,
                                                     arguments=args)
                else:
                    return_name = PeriodicTaskGenerator(
                        self.periodic_tasks_location).get_tasks()[self.__translate_periodic_task_id(args[0])].name
            else:
                self.tasks[int(args[0])].status = TaskStatus.done
                self.tasks[int(args[0])].date_finished = self.__get_today()
                self.__save_if_allowed()
                return_name = self.tasks[int(args[0])].name
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_done_ok,
                                             arguments=[return_name])
        except (IndexError, ValueError):
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_done_wrong_parameter,
                                             arguments=args)

    def __command_undone(self, args):
        try:
            if int(args[0]) > len(self.tasks):
                raise IndexError
            if int(args[0]) < 0:
                return_value = PeriodicTaskProgressHandler(self.periodic_tasks_location).set_undone(
                    self.__translate_periodic_task_id(int(args[0])))
                if return_value is None:
                    return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_done_wrong_parameter,
                                                     arguments=args)
                else:
                    return_name = PeriodicTaskGenerator(
                        self.periodic_tasks_location).get_tasks()[self.__translate_periodic_task_id(args[0])].name
            else:
                self.tasks[int(args[0])].status = TaskStatus.not_done
                self.__save_if_allowed()
                return_name = self.tasks[int(args[0])].name
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_undone_ok,
                                             arguments=[return_name])
        except (IndexError, ValueError):
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_done_wrong_parameter,
                                             arguments=args)

    def __command_periodic(self, args):
        return_list = []
        return_indexes = []
        tasks = PeriodicTaskGenerator(self.periodic_tasks_location).get_list_next_occurrence()
        for n, t in enumerate(tasks):
            return_list.append(t)
            return_indexes.append(self.__translate_periodic_task_id(n))
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_get, arguments=[return_indexes, return_list])

    def __command_bump(self, args):
        try:
            if int(args[0]) > len(self.tasks) or int(args[0]) < 0:
                raise IndexError
            self.tasks.append(self.tasks.pop(int(args[0])))
            self.__save_if_allowed()
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_bump_ok,
                                             arguments=[str(len(self.tasks) - 1), self.tasks[-1].name])
        except (IndexError, ValueError):
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.task_bump_nook,
                                             arguments=args)

    def __translate_periodic_task_id(self, task_id):
        return -(int(task_id)+1)

    def __sort_ls(self, tasks_tuple):
        try:
            tasks_tuple.sort(key=lambda tup: tup[1].date_to_finish, reverse=True)
        except TypeError:
            # This error occurs if task is set to today, then marked as done, and then 'set none' command is excuted, so
            # it stays visible in 'task ls', but has no date_to_finish
            # todo: handle such a case gently
            logging.error('Object has on date_to_finish set, but is sorted!')
        return_tuple = []
        for obj in tasks_tuple:
            if obj[1].status == TaskStatus.done:
                return_tuple.append(obj)
        for obj in tasks_tuple:

            if obj[1].status != TaskStatus.done:
                return_tuple.append(obj)
        return return_tuple
