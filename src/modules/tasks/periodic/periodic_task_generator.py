from src.interface.tasks.task_type import TaskType
from src.modules.tasks.periodic.periodic_task_loader import PeriodicTaskLoader
from src.modules.tasks.task_factory import TaskFactory
from src.utils.helpers import DateHelper


class PeriodicTaskGenerator:
    def __init__(self, filename):
        self.task_loader = PeriodicTaskLoader(filename)

    def get_tasks(self, time_delta=0):
        return_tasks = []
        target_day = DateHelper.get_today_short(time_delta)
        for periodic_task in self.task_loader.get():
            if periodic_task.is_to_be_reminded(target_day):
                return_tasks.append(TaskFactory().get_task(name=periodic_task.name,
                                                           date_to_finish=periodic_task.get_next_occurrence_as_date(time_delta),
                                                           task_type=TaskType.periodic,
                                                           reminder=periodic_task.reminder,
                                                           ))
        return return_tasks

    def get_list_next_occurrence(self):
        return_tasks = []
        for periodic_task in self.task_loader.get():
            return_tasks.append(TaskFactory().get_task(name=periodic_task.name,
                                                       date_to_finish=periodic_task.get_next_occurrence_as_date(),
                                                       task_type=TaskType.periodic,
                                                       reminder=periodic_task.reminder,
                                                       ))
        return return_tasks
