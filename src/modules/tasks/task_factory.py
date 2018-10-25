from src.interface.tasks.task import Task
from src.interface.tasks.task_priority import TaskPriority
from src.interface.tasks.task_status import TaskStatus
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
                 status=TaskStatus.unknown):
        return Task(name, description, date_added, date_to_finish, priority, task_type, status)
