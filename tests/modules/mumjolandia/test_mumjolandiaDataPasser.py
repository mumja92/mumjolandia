import threading
from queue import Queue
from unittest import TestCase
from unittest import mock
from unittest.mock import MagicMock

from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.mumjolandia_data_passer import MumjolandiaDataPasser


class TestMumjolandiaDataPasser(TestCase):
    @mock.patch('threading.Event.wait', return_value=None)
    @mock.patch('threading.Event.clear', return_value=None)
    def test_pass_command(self, mock_clear, mock_wait):
        qi = Queue()
        qo = Queue()
        qi.put = MagicMock(return_value=None)
        qo.get = MagicMock(return_value=MumjolandiaReturnValue.mumjolandia_exit)
        qo.task_done = MagicMock(return_value=None)
        mutex = threading.Lock()
        event = threading.Event()
        dp = MumjolandiaDataPasser(qi, qo, mutex, event)
        command = CommandFactory.get_command('xD')
        return_value = dp.pass_command(command)

        qi.put.assert_called_with(command)
        qo.get.assert_called_with()
        qo.task_done.assert_called_with()
        self.assertEqual(mock_wait.call_count, 1)
        self.assertEqual(mock_clear.call_count, 1)
        self.assertEqual(return_value, MumjolandiaReturnValue.mumjolandia_exit)
