from unittest import TestCase
from unittest.mock import patch

from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.command.command_factory import CommandFactory
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_supervisor import TaskSupervisor


class TestTaskSupervisor(TestCase):
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', side_effect=[[], [TaskFactory.get_task('simple task')]])
    def test_get_tasks(self, mock):
        ts = TaskSupervisor()
        self.assertEqual(len(ts.get_tasks()), 0)

        ts = TaskSupervisor()
        self.assertEqual(len(ts.get_tasks()), 1)
        self.assertEqual(ts.get_tasks(), [TaskFactory.get_task('simple task')])
        self.assertEqual(mock.call_count, 2)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_add_task(self, mock_save, mock_load):
        ts = TaskSupervisor()
        self.assertEqual(len(ts.get_tasks()), 0)

        ts.add_task('First task')
        self.assertEqual(len(ts.get_tasks()), 1)
        self.assertEqual(ts.get_tasks(), [TaskFactory.get_task('First task')])

        ts.add_task('Second task')
        self.assertEqual(ts.get_tasks(), [TaskFactory.get_task('First task'), TaskFactory.get_task('Second task')])
        self.assertEqual(mock_save.call_count, 2)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory.get_task('First task'),
                         TaskFactory.get_task('Second task'),
                         TaskFactory.get_task('Third task')])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_edit_task(self, mock_save, mock_load):
        ts = TaskSupervisor()
        self.assertEqual(len(ts.get_tasks()), 3)

        ts.edit_task(0, TaskFactory.get_task('Edited task'))
        self.assertEqual(ts.get_tasks(), [TaskFactory.get_task('Edited task'),
                                          TaskFactory.get_task('Second task'),
                                          TaskFactory.get_task('Third task')])

        ts.edit_task(-1, TaskFactory.get_task('Edited2 task'))
        self.assertEqual(mock_save.call_count, 2)
        self.assertEqual(ts.get_tasks(), [TaskFactory.get_task('Edited task'),
                                          TaskFactory.get_task('Second task'),
                                          TaskFactory.get_task('Edited2 task')])

        ts.edit_task(10, TaskFactory.get_task('Edited3 task'))
        self.assertEqual(mock_save.call_count, 2)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           side_effect=[[], [TaskFactory.get_task('First task'),
                             TaskFactory.get_task('Second task'),
                             TaskFactory.get_task('Second task'),
                             TaskFactory.get_task('Third task')]])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_delete_task(self, mock_save, mock_load):
        ts = TaskSupervisor()
        ts.delete_task(0)
        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

        ts = TaskSupervisor()
        ts.delete_task(3)
        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(ts.get_tasks(), [TaskFactory.get_task('First task'),
                                          TaskFactory.get_task('Second task'),
                                          TaskFactory.get_task('Second task')])

        ts.delete_task('Second task')
        self.assertEqual(mock_save.call_count, 2)
        self.assertEqual(ts.get_tasks(), [TaskFactory.get_task('First task')])

        ts.delete_task(0)
        self.assertEqual(mock_save.call_count, 3)
        self.assertEqual(len(ts.get_tasks()), 0)
        self.assertEqual(mock_load.call_count, 2)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory.get_task('Task')])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    @patch('logging.warning', return_value=None)
    def test_execute(self, mock_logging, mock_save, mock_load):
        ts = TaskSupervisor()

        response = ts.execute(CommandFactory.get_command(''))
        self.assertEqual(response.status, MumjolandiaReturnValue.mumjolandia_unrecognized_parameters)
        self.assertEqual(mock_logging.call_count, 1)

        response = ts.execute(CommandFactory.get_command('xD'))
        self.assertEqual(response.status, MumjolandiaReturnValue.mumjolandia_unrecognized_parameters)
        self.assertEqual(mock_logging.call_count, 2)

        response = ts.execute(CommandFactory.get_command("add 'new task'"))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_added)
        self.assertEqual(response.arguments, ['new task'])
        self.assertEqual(mock_save.call_count, 1)

        response = ts.execute(CommandFactory.get_command('get'))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_get)
        self.assertEqual(response.arguments, [TaskFactory.get_task('Task'), TaskFactory.get_task('new task')])

        response = ts.execute(CommandFactory.get_command('delete not_existing_task'))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_delete_incorrect_name)
        self.assertEqual(response.arguments, ['not_existing_task'])

        response = ts.execute(CommandFactory.get_command("delete 7"))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_delete_incorrect_index)
        self.assertEqual(response.arguments, ['7'])

        response = ts.execute(CommandFactory.get_command("delete 'new task'"))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_delete_success)
        self.assertEqual(response.arguments, ['new task', '1'])
        self.assertEqual(mock_save.call_count, 2)

        response = ts.execute(CommandFactory.get_command('get xD'))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_get_wrong_data)
        self.assertEqual(response.arguments, ['xD'])

        response = ts.execute(CommandFactory.get_command("edit 1 new"))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_edit_wrong_index)
        self.assertEqual(response.arguments, ['1'])
        self.assertEqual(mock_save.call_count, 2)

        response = ts.execute(CommandFactory.get_command("edit 0 new"))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_edit_ok)
        self.assertEqual(response.arguments, ['0'])
        self.assertEqual(mock_save.call_count, 3)

        response = ts.execute(CommandFactory.get_command("delete 0"))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_delete_success)
        self.assertEqual(response.arguments, ['0', '1'])
        self.assertEqual(mock_save.call_count, 4)

        response = ts.execute(CommandFactory.get_command('get'))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_get)
        self.assertEqual(response.arguments, [])

        response = ts.execute(CommandFactory.get_command('help'))
        self.assertEqual(response.status, MumjolandiaReturnValue.task_help)
        self.assertEqual(response.arguments, ['print, add [name], delete [name || id], edit [id] [name]'])

        self.assertEqual(mock_save.call_count, 4)
        self.assertEqual(mock_load.call_count, 1)
