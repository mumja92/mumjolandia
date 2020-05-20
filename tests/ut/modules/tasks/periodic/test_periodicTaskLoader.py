import logging
from unittest import TestCase

from src.interface.tasks.periodic.periodic_task import PeriodicTaskOccurrenceType
from src.modules.tasks.periodic.periodic_task_loader import PeriodicTaskLoader


class TestPeriodicTaskLoader(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPeriodicTaskLoader, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def test_get_events_ok(self):
        # tasks = PeriodicTaskLoader('abc', 'data/test_periodic_task_loader_data.xml').get()    # for local run
        tasks = PeriodicTaskLoader('abc', 'ut/modules/tasks/periodic/data/test_periodic_task_loader_data.xml').get()

        self.assertEqual(len(tasks), 2)

        self.assertEqual(tasks[0].name, 'event1')
        self.assertEqual(tasks[0].reminder, 3)
        self.assertEqual(tasks[0].occurrence_type, PeriodicTaskOccurrenceType.year)
        self.assertEqual(tasks[0].start.day, 12)
        self.assertEqual(tasks[0].start.month, 5)

        self.assertEqual(tasks[1].name, 'event2')
        self.assertEqual(tasks[1].reminder, 3)
        self.assertEqual(tasks[1].occurrence_type, PeriodicTaskOccurrenceType.year)
        self.assertEqual(tasks[1].start.day, 10)
        self.assertEqual(tasks[1].start.month, 1)
