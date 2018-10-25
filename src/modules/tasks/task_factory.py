from src.interface.tasks.task import Task
from src.interface.tasks.task_occurrence import TaskOccurrence
from src.interface.tasks.task_priority import TaskPriority
from src.interface.tasks.task_type import TaskType
import datetime


class TaskFactory:
    @staticmethod
    def get_task(name='none',
                 description='none',
                 date_added=datetime.date.today(),
                 date_to_finish=datetime.date.today(),
                 priority=TaskPriority.unknown,
                 task_type=TaskType.normal,
                 occurrence=TaskOccurrence.once,
                 occurrence_list=None):
        return Task(name, description, date_added, date_to_finish, priority, task_type, occurrence, occurrence_list)
