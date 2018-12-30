from src.interface.tasks.task import Task
from src.interface.mumjolandia.incorrect_date_format_exception import IncorrectDateFormatException
from src.interface.tasks.task_priority import TaskPriority
from src.interface.tasks.task_status import TaskStatus
from src.interface.tasks.task_type import TaskType
import datetime


class TaskFactory:
    @staticmethod
    def get_task(name='unknown',
                 description='unknown',
                 date_added=datetime.datetime.today().replace(microsecond=0),
                 date_to_finish=datetime.datetime.today().replace(microsecond=0),
                 priority=TaskPriority.unknown,
                 task_type=TaskType.unknown,
                 status=TaskStatus.unknown):
        try:
            if isinstance(date_added, str):
                date_added = datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
            if isinstance(date_to_finish, str):
                date_to_finish = datetime.datetime.strptime(date_to_finish, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise IncorrectDateFormatException
        return Task(name, description, date_added, date_to_finish, priority, task_type, status)
