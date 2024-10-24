import logging
import threading
from queue import Queue
from unittest import TestCase

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread


class MumjolandiaTest(TestCase):
    def __init__(self, *args, **kwargs):
        super(MumjolandiaTest, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True
        self.mumjolandia_thread = None
        self.command_queue_request = Queue()
        self.command_queue_response = Queue()
        self.command_responded_event = threading.Event()
        self.mumjolandia_thread = MumjolandiaThread(self.command_queue_request,
                                                    self.command_queue_response,
                                                    self.command_responded_event)
        self.mumjolandia_thread.setName('mumjolandia test thread')

    def setUp(self):
        self.assertEqual(self.command_queue_request.qsize(), 0)
        self.assertEqual(self.command_queue_response.qsize(), 0)
        self.assertEqual(self.command_responded_event.isSet(), 0)
        self.assertEqual(self.mumjolandia_thread.is_alive(), False)
        self.mumjolandia_thread.start()

    def tearDown(self):
        self.send_command("exit")
        self.mumjolandia_thread.join()
        if self.mumjolandia_thread.is_alive():
            self.fail("Thread didn't stop in time")
        self.mumjolandia_thread = None
        self.command_queue_request.empty()
        self.command_queue_response.empty()
        self.command_responded_event.clear()

    def send_command(self, command: str) -> MumjolandiaResponseObject:
        self.command_queue_request.put(CommandFactory().get_command(command))
        self.command_responded_event.wait()
        self.command_responded_event.clear()
        return self.command_queue_response.get()
