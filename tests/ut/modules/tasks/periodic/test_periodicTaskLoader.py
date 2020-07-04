import logging
from unittest import TestCase

from src.interface.tasks.periodic.periodic_task import PeriodicTaskOccurrenceType
from src.modules.tasks.periodic.periodic_task_loader import PeriodicTaskLoader


class TestPeriodicTaskLoader(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPeriodicTaskLoader, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def test_get_events_ok(self):
        pass
        # todo: add tests
