import logging
from queue import Queue
from src.interface.tasks.task_storage_type import StorageType
from src.modules.command.command_factory import CommandFactory
from src.modules.mumjolandia.mumjolandia_data_passer import MumjolandiaDataPasser
from src.modules.mumjolandia.mumjolandia_thread import MumjolandiaThread
from src.modules.mumjolandia.ui.mumjolandia_cli import MumjolandiaCli
from src.modules.mumjolandia.ui.mumjolandia_gui import MumjolandiaGui
from src.modules.tasks.task_supervisor import TaskSupervisor


class MumjolandiaSupervisor:
    def __init__(self):
        self.log_location = 'data/log.log'
        self.command_queue_input = Queue()      # commands shared with ui (user input)
        self.command_queue_output = Queue()     # commands shared with mumjolandia_thread
        self.supervisors = {}
        self.data_passer = MumjolandiaDataPasser(self.supervisors, self.command_queue_input)
        self.__run_init()

    def run_gui(self):
        logging.info('Starting GUI')
        self.__run_mumjolandia()
        gui = MumjolandiaGui(self.data_passer)
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
        mumjolandia_thread = MumjolandiaThread(self.command_queue_output, self.supervisors)
        mumjolandia_thread.setName('mumjolandia thread')
        mumjolandia_thread.start()

    def __main_loop(self):
        while True:
            command = self.command_queue_input.get()
            self.command_queue_input.task_done()
            logging.info('Parsing command: ' + str(command))
            self.command_queue_output.put(command)
            if command.arguments[0] == 'exit':
                logging.info('exiting')
                break

    def __run_init(self):
        logging.basicConfig(format='%(asctime)s [%(levelname).1s] %(module)s::%(funcName)s --- %(message)s',
                            datefmt='%d/%m/%Y %H:%M:%S', filename=self.log_location, level=logging.DEBUG)
        self.supervisors['task'] = TaskSupervisor(storage_type=StorageType.xml)
