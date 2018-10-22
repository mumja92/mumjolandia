import datetime
from src.modules.tasks.task import Task


class TaskFactory:
    @staticmethod
    def get_task(name, priority, date=datetime.date.today()):
        return Task(name, date, priority)
