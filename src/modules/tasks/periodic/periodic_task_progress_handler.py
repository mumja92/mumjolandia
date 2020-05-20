import datetime

from src.interface.tasks.task_type import TaskType
from src.modules.tasks.periodic.periodic_task_generator import PeriodicTaskGenerator
from src.utils.helpers import DateHelper
from src.utils.shared_preferences import SharedPreferences


# todo: when xml file with periodic tasks changes, indexes of tasks will be incorrect until the next day


class PeriodicTaskProgressHandler:
    def __init__(self, periodic_filename, event_filename):
        self.periodic_file = periodic_filename
        self.event_filename = event_filename
        self.tasks_prefix = 'periodic_tasks_data_'

    def set_done(self, task_id):
        return_value = False
        self.__handle_date_progression()
        tasks = PeriodicTaskGenerator(self.periodic_file, self.event_filename).get_tasks()
        try:
            if 0 <= task_id < len(tasks):
                return_value = SharedPreferences().put(self.__generate_preference_string(tasks[task_id].name),
                                                       str(tasks[task_id].date_to_finish))
        except TypeError:   # len(tasks) is Null
            pass
        return return_value

    def set_undone(self, task_id):
        return_value = None
        self.__handle_date_progression()
        tasks = PeriodicTaskGenerator(self.periodic_file, self.event_filename).get_tasks()
        try:
            if 0 <= task_id < len(tasks):
                return_value = SharedPreferences().clear_key(self.__generate_preference_string(tasks[task_id].name))
        except TypeError:  # len(tasks) is Null
            pass
        return return_value

    def is_done(self, task_id):
        return_value = False
        self.__handle_date_progression()
        tasks = PeriodicTaskGenerator(self.periodic_file, self.event_filename).get_tasks()
        try:
            if 0 <= task_id < len(tasks):
                if SharedPreferences().get(self.__generate_preference_string(tasks[task_id].name)):
                    return_value = True
        except TypeError:  # len(tasks) is Null
            pass
        return return_value

    def reset(self):
        SharedPreferences().clear_starting_pattern(self.tasks_prefix)

    def __handle_date_progression(self):
        tasks = PeriodicTaskGenerator(self.periodic_file, self.event_filename).get_tasks()
        for task_id, task in enumerate(tasks):
            saved_value = SharedPreferences().get(self.__generate_preference_string(task.name))
            if saved_value is not None:
                if task.type is TaskType.event:
                    if datetime.datetime.strptime(saved_value[:], '%Y-%m-%d').date().year < DateHelper.get_today_short().year:
                        SharedPreferences().clear_key(self.__generate_preference_string(task.name))
                else:
                    if task.date_to_finish > datetime.datetime.strptime(saved_value[:], '%Y-%m-%d').date():
                        SharedPreferences().clear_key(self.__generate_preference_string(task.name))

    def __generate_preference_string(self, value):
        return self.tasks_prefix + str(value)
