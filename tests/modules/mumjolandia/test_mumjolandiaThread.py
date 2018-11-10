import threading
from queue import Queue
from unittest import TestCase
from unittest.mock import patch, MagicMock

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread


class TestMumjolandiaThread(TestCase):
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def setUp(self, mock_task_save, mock_task_get):
        self.q1 = Queue()
        self.q1.task_done = MagicMock(return_value=None)
        self.q2 = Queue()
        self.event = threading.Event()
        self.mt = MumjolandiaThread(self.q1, self.q2, self.event)
        self.mt.exit_flag = True
        self.assertEqual(mock_task_save.call_count, 0)
        self.assertEqual(mock_task_get.call_count, 1)

    def tearDown(self):
        self.assertEqual(self.q2.qsize(), 0)

    @patch('logging.warning', return_value=None)
    @patch('src.modules.tasks.task_supervisor.TaskSupervisor.execute', return_value='not important, just passing by')
    def test_task(self, mock_task_supervisor, mock_logging):
        self.q1.get = MagicMock(return_value=CommandFactory.get_command('task'))
        self.mt.run()
        self.assertEqual(mock_task_supervisor.call_count, 1)
        self.assertEqual(self.q2.get(), 'not important, just passing by')

    @patch('logging.warning', return_value=None)
    @patch('src.modules.food.food_supervisor.FoodSupervisor.execute', return_value='not important, just passing by')
    def test_food(self, mock_food_supervisor, mock_logging):
        self.q1.get = MagicMock(return_value=CommandFactory.get_command('food print'))
        self.mt.run()
        self.assertEqual(mock_food_supervisor.call_count, 1)
        self.assertEqual(self.q2.get(), 'not important, just passing by')

    @patch('logging.warning', return_value=None)
    def test_unrecognized(self, mock_logging):
        self.q1.get = MagicMock(return_value=CommandFactory.get_command('unrecognized command'))
        self.mt.run()
        self.assertEqual(self.q2.get(),
                         MumjolandiaResponseObject(MumjolandiaReturnValue.mumjolandia_unrecognized_command,
                                                   CommandFactory.get_command('unrecognized command')))

    @patch('logging.warning', return_value=None)
    def test_exit(self, mock_logging):
        self.q1.get = MagicMock(return_value=CommandFactory.get_command('exit'))
        self.mt.run()
        self.assertEqual(self.q2.get(),
                         MumjolandiaResponseObject(status=MumjolandiaReturnValue.mumjolandia_exit))

    @patch('logging.warning', return_value=None)
    @patch('src.modules.tasks.task_supervisor.TaskSupervisor.execute', return_value=None)
    @patch('src.modules.food.food_supervisor.FoodSupervisor.execute', return_value=None)
    def test_sanity_supervisors_not_called(self, mock_food, mock_task, mock_logging):
        self.q1.get = MagicMock(return_value=CommandFactory.get_command(''))
        self.mt.run()
        self.assertEqual(self.q2.get(),
                         MumjolandiaResponseObject(MumjolandiaReturnValue.mumjolandia_unrecognized_command,
                                                   CommandFactory.get_command('')))
        self.assertEqual(mock_food.call_count, 0)
        self.assertEqual(mock_task.call_count, 0)
