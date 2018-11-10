import datetime
from unittest import TestCase
from src.interface.mumjolandia.incorrect_date_format_exception import IncorrectDateFormatException
from src.interface.tasks.task_priority import TaskPriority
from src.interface.tasks.task_status import TaskStatus
from src.interface.tasks.task_type import TaskType
from src.modules.tasks.task_factory import TaskFactory


class TestTaskFactory(TestCase):
    def test_get_task_empty(self):
        t = TaskFactory.get_task()
        self.assertEqual(t.name, 'unknown')
        self.assertEqual(t.description, 'unknown')
        self.assertEqual(t.date_added, datetime.date.today())
        self.assertEqual(t.date_to_finish, datetime.date.today())
        self.assertEqual(t.priority, TaskPriority['unknown'])
        self.assertEqual(t.type, TaskType['unknown'])
        self.assertEqual(t.status, TaskStatus['unknown'])

    def test_get_task_with_parameters(self):
        test_date_added = datetime.datetime.strptime("2018-10-25 00:00:00", '%Y-%m-%d %H:%M:%S')
        test_date_to_finish = datetime.datetime.strptime("2019-10-26 00:00:00", '%Y-%m-%d %H:%M:%S')
        t = TaskFactory.get_task(name='żółć xD',
                                 description='brak',
                                 date_added="2018-10-25 00:00:00",
                                 date_to_finish="2019-10-26 00:00:00",
                                 priority=TaskPriority.ez,
                                 task_type=TaskType.normal,
                                 status=TaskStatus.not_done)
        self.assertEqual(t.name, 'żółć xD')
        self.assertEqual(t.description, 'brak')
        self.assertEqual(t.date_added, test_date_added)
        self.assertEqual(t.date_to_finish, test_date_to_finish)
        self.assertEqual(t.priority, TaskPriority.ez)
        self.assertEqual(t.type, TaskType.normal)
        self.assertEqual(t.status, TaskStatus.not_done)

    def test_incorrect_date_format_exception_raised(self):
        with self.assertRaises(IncorrectDateFormatException):
            TaskFactory.get_task(date_added="12.11.2018")
