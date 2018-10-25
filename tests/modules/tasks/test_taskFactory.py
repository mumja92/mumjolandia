from unittest import TestCase

from src.interface.tasks.task_priority import TaskPriority
from src.modules.tasks.task_factory import TaskFactory


class TestTaskFactory(TestCase):
    def test_get_task(self):
        t = TaskFactory.get_task('żółć xD', TaskPriority.ez)
        self.assertEquals(t.text, 'żółć xD')
        t = TaskFactory.get_task('', TaskPriority.ez)
        self.assertEquals(t.text, '')
