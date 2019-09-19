import datetime

from src.modules.tasks.periodic_tasks_generator import PeriodicTasksGenerator
from src.utils.shared_preferences import SharedPreferences


# todo: when xml file with periodic tasks changes, indexes of tasks will be incorrect until the next day


class PeriodicTaskProgressHandler:
    def __init__(self, filename):
        self.file = filename
        self.tasks_date_string = 'periodic_tasks_date_today'
        self.tasks_prefix = 'periodic_tasks_data_'

    def set_done(self, task_id):
        return_value = False
        self.__handle_date_progression()
        tasks = PeriodicTasksGenerator(self.file).get_tasks()
        try:
            if 0 <= task_id < len(tasks):
                return_value = SharedPreferences().put(self.__generate_preference_string(task_id), 'true')
        except TypeError:   # len(tasks) is Null
            pass
        return return_value

    def set_undone(self, task_id):
        return_value = None
        self.__handle_date_progression()
        tasks = PeriodicTasksGenerator(self.file).get_tasks()
        try:
            if 0 <= task_id < len(tasks):
                return_value = SharedPreferences().clear_key(self.__generate_preference_string(task_id))
        except TypeError:  # len(tasks) is Null
            pass
        return return_value

    def is_done(self, task_id):
        return_value = False
        self.__handle_date_progression()
        tasks = PeriodicTasksGenerator(self.file).get_tasks()
        try:
            if 0 <= task_id < len(tasks):
                if SharedPreferences().get(self.__generate_preference_string(task_id)) == 'true':
                    return_value = True
        except TypeError:  # len(tasks) is Null
            pass
        return return_value

    def reset(self):
        SharedPreferences().clear_starting_pattern(self.tasks_prefix)
        SharedPreferences().clear_key(self.tasks_date_string)

    def __handle_date_progression(self):
        sp = SharedPreferences()
        date_today = datetime.date.today()
        try:
            date_preferences = datetime.datetime.strptime(sp.get(self.tasks_date_string), '%Y-%m-%d').date()
        except TypeError:
            date_preferences = None
        if date_preferences is None:
            sp.put(self.tasks_date_string, str(date_today))
        elif date_today > date_preferences:
            sp.clear_starting_pattern(self.tasks_prefix)
            sp.put(self.tasks_date_string, str(date_today))

    def __generate_preference_string(self, value):
        return self.tasks_prefix + str(value)
