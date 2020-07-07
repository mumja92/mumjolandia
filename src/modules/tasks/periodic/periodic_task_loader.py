import logging
from pathlib import Path

import datetime

from src.external.xmltodict import xmltodict
from src.interface.tasks.periodic.periodic_task import PeriodicTaskOccurrenceType
from src.interface.tasks.task_type import TaskType
from src.modules.tasks.periodic.periodic_task_factory import PeriodicTaskFactory


class PeriodicTaskLoader:
    def __init__(self, periodic_filename, event_filename, event_reminder=7):
        self.periodic_file = periodic_filename
        self.event_file = event_filename
        self.event_reminder = event_reminder
        self.tasks = self.__get_tasks_events() + self.__get_tasks_periodic()

    def get(self):
        # todo: add check if there isn't the same name in periodic tasks and events
        return self.tasks

    def __get_tasks_periodic(self):
        tasks = []
        file = Path(self.periodic_file)
        if file.is_file():
            with open(self.periodic_file, 'r') as my_file:
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

    def __get_tasks_events(self):
        tasks = []
        file = Path(self.event_file)
        if file.is_file():
            with open(self.event_file, 'r') as file:
                data = file.read()
            d = xmltodict.parse(data)
            occurrence_type = PeriodicTaskOccurrenceType.year
            occurrence = 1
            reminder = self.event_reminder
            try:
                if len(d['events']['event']) == 1:
                    start = datetime.datetime.strptime(str(datetime.datetime.now().year) + '-' + d['events']['event']['date'], '%Y-%d-%m').date()
                    tasks.append(PeriodicTaskFactory.get_periodic_task(name=d['events']['event']['name'],
                                                                       occurrence_type=occurrence_type,
                                                                       occurrence=occurrence,
                                                                       reminder=reminder,
                                                                       start=start,
                                                                       task_type=TaskType.event,
                                                                       ))
                else:
                    for event in d['events']['event']:
                        start = datetime.datetime.strptime(str(datetime.datetime.now().year) + '-' + event['date'], '%Y-%d-%m').date()
                        tasks.append(PeriodicTaskFactory.get_periodic_task(name=event['name'],
                                                                           occurrence_type=occurrence_type,
                                                                           occurrence=occurrence,
                                                                           reminder=reminder,
                                                                           start=start,
                                                                           task_type=TaskType.event,
                                                                           ))
            except TypeError:
                # todo: investigate
                logging.error("Type error in events, please investigate")
                return tasks
        else:
            logging.error("Event file doesn't exist")
        return tasks
