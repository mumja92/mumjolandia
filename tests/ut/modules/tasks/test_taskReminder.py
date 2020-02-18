from unittest import TestCase

from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_reminder import TaskReminder
from src.utils.helpers import DateHelper


# todo: change dates to fixed
class TestTaskReminder(TestCase):
    def test_should_be_reminded_true_ok(self):
        date1 = DateHelper.get_today_short(3)
        task = TaskFactory.get_task(date_to_finish=DateHelper.get_today_short(5), reminder=2)
        self.assertTrue(TaskReminder.should_be_reminded(task, date1))

    def test_should_be_reminded_false_ok(self):
        date1 = DateHelper.get_today_short(2)
        task = TaskFactory.get_task(date_to_finish=DateHelper.get_today_short(5), reminder=2)
        self.assertFalse(TaskReminder.should_be_reminded(task, date1))

    def test_should_be_reminded_negative_value_true_ok(self):
        date1 = DateHelper.get_today_short(8)
        task = TaskFactory.get_task(date_to_finish=DateHelper.get_today_short(5), reminder=2)
        self.assertTrue(TaskReminder.should_be_reminded(task, date1))

    def test_should_be_reminded_default_date_true_ok(self):
        task = TaskFactory.get_task(date_to_finish=DateHelper.get_today_short(3), reminder=3)
        self.assertTrue(TaskReminder.should_be_reminded(task))

    def test_should_be_reminded_default_date_false_ok(self):
        task = TaskFactory.get_task(date_to_finish=DateHelper.get_today_short(3), reminder=2)
        self.assertFalse(TaskReminder.should_be_reminded(task))
