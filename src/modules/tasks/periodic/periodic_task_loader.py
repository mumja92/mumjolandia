from pathlib import Path

import datetime

from src.external.xmltodict import xmltodict
from src.interface.tasks.periodic.periodic_task import PeriodicTaskOccurrenceType
from src.modules.tasks.periodic.periodic_task_factory import PeriodicTaskFactory


class PeriodicTaskLoader:
    def __init__(self, filename):
        self.file = filename

    def get(self):
        tasks = []
        file = Path(self.file)
        if not file.is_file():
            return []
        with open(self.file, 'r') as my_file:
            data = my_file.read()
        d = xmltodict.parse(data)
        for t in d['tasks']['task']:
            name = t['name']
            occurrence_type = PeriodicTaskOccurrenceType.day
            if t['occurrence_type'] == 'week':
                occurrence_type = PeriodicTaskOccurrenceType.week
            occurrence = t['occurrence']
            reminder = t['reminder']
            start = datetime.datetime.strptime(t['start'], '%Y-%m-%d').date()
            tasks.append(PeriodicTaskFactory.get_periodic_task(name=name,
                                                               occurrence_type=occurrence_type,
                                                               occurrence=occurrence,
                                                               reminder=reminder,
                                                               start=start,
                                                               ))
        return tasks
