import logging
from unittest import TestCase
from unittest.mock import patch

from src.interface.tasks.periodic.periodic_task import PeriodicTaskOccurrenceType
from src.modules.tasks.periodic.periodic_task_factory import PeriodicTaskFactory
from tests.ut.helpers.helpers import DateTimeHelper


class TestPeriodicTask(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPeriodicTask, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def test_get_next_occurrence_day1_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.day,
                                                     occurrence=5,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-7),
                                                     )
        self.assertEqual(task.get_next_occurrence_in_days_as_int(DateTimeHelper.get_fixed_date(2)), 1)

    def test_get_next_occurrence_day2_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.day,
                                                     occurrence=5,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-7),
                                                     )
        self.assertEqual(task.get_next_occurrence_in_days_as_int(DateTimeHelper.get_fixed_date(3)), 0)

    def test_get_next_occurrence_day3_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.day,
                                                     occurrence=5,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-7),
                                                     )
        self.assertEqual(task.get_next_occurrence_in_days_as_int(DateTimeHelper.get_fixed_date(4)), 4)

    def test_get_next_occurrence_week1_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.week,
                                                     occurrence=2,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertEqual(task.get_next_occurrence_in_days_as_int(DateTimeHelper.get_fixed_date(7)), 1)

    def test_get_next_occurrence_week2_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.week,
                                                     occurrence=2,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertEqual(task.get_next_occurrence_in_days_as_int(DateTimeHelper.get_fixed_date(8)), 0)

    def test_get_next_occurrence_week3_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.week,
                                                     occurrence=2,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertEqual(task.get_next_occurrence_in_days_as_int(DateTimeHelper.get_fixed_date(9)), 13)

    def test_is_to_be_reminded_week1_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.week,
                                                     occurrence=2,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertFalse(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(5)))

    def test_is_to_be_reminded_week2_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.week,
                                                     occurrence=2,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertTrue(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(6)))

    def test_is_to_be_reminded_week3_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.week,
                                                     occurrence=2,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertTrue(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(7)))

    def test_is_to_be_reminded_week4_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.week,
                                                     occurrence=2,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertTrue(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(8)))

    def test_is_to_be_reminded_week5_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.week,
                                                     occurrence=2,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertFalse(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(9)))

    def test_is_to_be_reminded_day1_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.day,
                                                     occurrence=5,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertFalse(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(1)))

    def test_is_to_be_reminded_day2_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.day,
                                                     occurrence=5,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertTrue(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(2)))

    def test_is_to_be_reminded_day3_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.day,
                                                     occurrence=5,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertTrue(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(3)))

    def test_is_to_be_reminded_day4_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.day,
                                                     occurrence=5,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertTrue(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(4)))

    def test_is_to_be_reminded_day5_ok(self):
        task = PeriodicTaskFactory.get_periodic_task(name='task1',
                                                     occurrence_type=PeriodicTaskOccurrenceType.day,
                                                     occurrence=5,
                                                     reminder=2,
                                                     start=DateTimeHelper.get_fixed_date(-6),
                                                     )
        self.assertFalse(task.is_to_be_reminded(DateTimeHelper.get_fixed_date(5)))
