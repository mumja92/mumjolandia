import logging
from unittest import TestCase
from unittest.mock import patch

from src.interface.tasks.periodic.periodic_task import PeriodicTaskOccurrenceType
from src.modules.tasks.periodic.periodic_task_factory import PeriodicTaskFactory
from src.modules.tasks.periodic.periodic_task_generator import PeriodicTaskGenerator
from src.modules.tasks.periodic.periodic_task_loader import PeriodicTaskLoader
from tests.ut.helpers.helpers import DateTimeHelper


class TestPeriodicTaskGenerator(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPeriodicTaskGenerator, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True

    def setUp(self):
        self.patcher_date_long = patch('src.utils.helpers.DateHelper.get_today_long')
        self.mock_date_long = self.patcher_date_long.start()
        self.mock_date_long.side_effect = lambda date_shift=0: DateTimeHelper.get_fixed_datetime(date_shift)
        self.addCleanup(self.patcher_date_long.stop)

        self.patcher_date_short = patch('src.utils.helpers.DateHelper.get_today_short')
        self.mock_date_short = self.patcher_date_short.start()
        self.mock_date_short.side_effect = lambda date_shift=0: DateTimeHelper.get_fixed_date(date_shift)
        self.addCleanup(self.patcher_date_short.stop)

    test_data = [
        PeriodicTaskFactory().get_periodic_task(
            name='task1',
            occurrence_type=PeriodicTaskOccurrenceType.day,
            occurrence=5,
            reminder=2,
            start=DateTimeHelper.get_fixed_date(-1),
        ),
        PeriodicTaskFactory().get_periodic_task(
            name='task2',
            occurrence_type=PeriodicTaskOccurrenceType.day,
            occurrence=11,
            reminder=1,
            start=DateTimeHelper.get_fixed_date(10),
        ),
        PeriodicTaskFactory().get_periodic_task(
            name='task3',
            occurrence_type=PeriodicTaskOccurrenceType.week,
            occurrence=2,
            reminder=1,
            start=DateTimeHelper.get_fixed_date(-5),
        ),
        PeriodicTaskFactory().get_periodic_task(
            name='task4',
            occurrence_type=PeriodicTaskOccurrenceType.week,
            occurrence=1,
            reminder=3,
            start=DateTimeHelper.get_fixed_date(8),
        ),
    ]

    @patch.object(PeriodicTaskLoader, 'get', return_value=test_data)
    def test_get_list_next_occurrence_ok(self, mock_load):
        ptg = PeriodicTaskGenerator('test')
        returned_tasks = ptg.get_list_next_occurrence()

        self.assertTrue(self.mock_date_short.called)
        self.assertTrue(self.mock_date_long.called)
        self.assertEqual(mock_load.call_count, 1)
        self.assertEqual(len(returned_tasks), 4)

        self.assertEqual(returned_tasks[0].date_to_finish, DateTimeHelper.get_fixed_date(4))
        self.assertEqual(returned_tasks[1].date_to_finish, DateTimeHelper.get_fixed_date(10))
        self.assertEqual(returned_tasks[2].date_to_finish, DateTimeHelper.get_fixed_date(9))
        self.assertEqual(returned_tasks[3].date_to_finish, DateTimeHelper.get_fixed_date(8))

    @patch.object(PeriodicTaskLoader, 'get', return_value=test_data)
    def test_get_tasks_without_shift_ok(self, mock_load):
        ptg = PeriodicTaskGenerator('test')
        returned_tasks = ptg.get_tasks()

        self.assertEqual(mock_load.call_count, 1)
        self.assertEqual(len(returned_tasks), 0)

    @patch.object(PeriodicTaskLoader, 'get', return_value=test_data)
    def test_get_tasks_with_shift_7_ok(self, mock_load):
        ptg = PeriodicTaskGenerator('test')
        returned_tasks = ptg.get_tasks(7)

        self.assertTrue(self.mock_date_short.called)
        self.assertTrue(self.mock_date_long.called)
        self.assertEqual(mock_load.call_count, 1)
        self.assertEqual(len(returned_tasks), 2)

        self.assertEqual(returned_tasks[0].name, 'task1')
        self.assertEqual(returned_tasks[1].name, 'task4')

    @patch.object(PeriodicTaskLoader, 'get', return_value=test_data)
    def test_get_tasks_with_shift_8_ok(self, mock_load):
        ptg = PeriodicTaskGenerator('test')
        returned_tasks = ptg.get_tasks(8)

        self.assertTrue(self.mock_date_short.called)
        self.assertTrue(self.mock_date_long.called)
        self.assertEqual(mock_load.call_count, 1)
        self.assertEqual(len(returned_tasks), 3)

        self.assertEqual(returned_tasks[0].name, 'task1')
        self.assertEqual(returned_tasks[1].name, 'task3')
        self.assertEqual(returned_tasks[2].name, 'task4')

    @patch.object(PeriodicTaskLoader, 'get', return_value=test_data)
    def test_get_tasks_with_shift_9_ok(self, mock_load):
        ptg = PeriodicTaskGenerator('test')
        returned_tasks = ptg.get_tasks(9)

        self.assertTrue(self.mock_date_short.called)
        self.assertTrue(self.mock_date_long.called)
        self.assertEqual(mock_load.call_count, 1)
        self.assertEqual(len(returned_tasks), 3)

        self.assertEqual(returned_tasks[0].name, 'task1')
        self.assertEqual(returned_tasks[1].name, 'task2')
        self.assertEqual(returned_tasks[2].name, 'task3')

    @patch.object(PeriodicTaskLoader, 'get', return_value=test_data)
    def test_get_tasks_with_shift_10_ok(self, mock_load):
        ptg = PeriodicTaskGenerator('test')
        returned_tasks = ptg.get_tasks(10)

        self.assertTrue(self.mock_date_short.called)
        self.assertTrue(self.mock_date_long.called)
        self.assertEqual(mock_load.call_count, 1)
        self.assertEqual(len(returned_tasks), 1)

        self.assertEqual(returned_tasks[0].name, 'task2')
