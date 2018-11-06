from unittest import TestCase
from unittest.mock import patch

from src.modules.tasks.task_loader_xml import TaskLoaderXml
from src.modules.tasks.task_supervisor import TaskSupervisor


class TestTaskSupervisor(TestCase):
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get_tasks', return_value=['xD'])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save_tasks', return_value=None)
    def test_get_tasks(self, mock, mock2):
        ts = TaskSupervisor()
        self.assertEqual(ts.get_tasks(), ['xD'])
        ts.add_task('xD')
        self.assertEqual(mock.called, True)
        self.assertEqual(mock2.called, True)

    # def test_add_task(self):
    #     self.fail()
    #
    # def test_edit_task(self):
    #     self.fail()
    #
    # def test_delete_task(self):
    #     self.fail()
    #
    # def test_execute(self):
    #     self.fail()
