import datetime
from pathlib import Path

from src.interface.tasks.task_type import TaskType
from src.modules.tasks.task_factory import TaskFactory
from src.utils import xmltodict


class PeriodicTasksGenerator:
    def __init__(self, filename):
        self.file = filename

    def get_tasks(self, time_delta=0):
        tasks = []
        file = Path(self.file)
        if not file.is_file():
            return []
        with open(self.file, 'r') as my_file:
            data = my_file.read()
        d = xmltodict.parse(data)
        for t in d['tasks']['task']:
            today = datetime.datetime.today().replace(microsecond=0)
            start = datetime.datetime.strptime(t['start'], '%Y-%m-%d %H:%M:%S')
            delta = today - start
            if t['occurrence_type'] == 'day':
                if ((delta.days + time_delta) % int(t['occurrence'])) == 0:
                    tasks.append(TaskFactory().get_task(name=t['name'],
                                                        date_to_finish=today,
                                                        task_type=TaskType.periodic))
            if t['occurrence_type'] == 'week':
                if ((delta.days + time_delta) % (int(t['occurrence']))*7) == 0:
                    tasks.append(TaskFactory().get_task(name=t['name'],
                                                        date_to_finish=today,
                                                        task_type=TaskType.periodic))
        return tasks
