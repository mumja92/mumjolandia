from unittest import TestCase
from src.modules.tasks.task_factory import TaskFactory


class TestTaskFactory(TestCase):
    def test_get_task(self):
        self.assertEquals(TaskFactory.get_task('żółć xD').text, 'żółć xD')
        self.assertEquals(TaskFactory.get_task('').text, '')
