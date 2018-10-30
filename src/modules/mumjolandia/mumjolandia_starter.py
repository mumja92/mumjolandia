import logging
import threading
from queue import Queue

from src.interface.tasks.task_storage_type import StorageType
from src.modules.mumjolandia.mumjolandia_data_passer import MumjolandiaDataPasser
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.ui.mumjolandia_cli import MumjolandiaCli
from src.modules.mumjolandia.ui.mumjolandia_gui import MumjolandiaGui
from src.modules.tasks.task_supervisor import TaskSupervisor


class MumjolandiaStarter:
    def __init__(self):
        self.log_location = 'data/log.log'
        self.command_queue_request = Queue()
        self.command_queue_response = Queue()
        self.supervisors = {}
        self.command_responded_event = threading.Event()
        self.data_passer = None
        self.command_mutex = threading.Lock()
        self.__run_init()

    def run_gui(self):
        logging.info('Starting GUI')
        self.__run_mumjolandia()
        gui = MumjolandiaGui(self.data_passer)  # not implemented yet
        gui.run()
        self.__main_loop()

    def run_cli(self):
        logging.info('Starting CLI')
        self.__run_mumjolandia()
        cli = MumjolandiaCli(self.data_passer)
        cli.setName('cli thread')
        cli.start()
        self.__main_loop()


    def __run_mumjolandia(self):
        logging.info('Starting mumjolandia')
        mumjolandia_thread = MumjolandiaThread(self.command_queue_request,
                                               self.command_queue_response,
                                               self.supervisors,
                                               self.command_responded_event)
        mumjolandia_thread.setName('mumjolandia thread')
        mumjolandia_thread.start()

    def __main_loop(self):
        logging.info('All tasks started. Exiting. ')

    def __run_init(self):
        logging.basicConfig(format='%(asctime)s [%(levelname).1s] %(module)s::%(funcName)s --- %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S', filename=self.log_location, level=logging.DEBUG)

        self.supervisors['task'] = TaskSupervisor(storage_type=StorageType.xml)

        self.data_passer = MumjolandiaDataPasser(self.supervisors,
                                                 self.command_queue_request,
                                                 self.command_queue_response,
                                                 self.command_mutex,
                                                 self.command_responded_event)
