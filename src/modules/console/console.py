import threading

from src.modules.command.command_factory import CommandFactory


class Console:
    def __init__(self):
        self.command_factory = CommandFactory()
        self.async_command = None
        self.thread = None

    def get_next_command(self):
        return self.command_factory.get_command(input())

    def get_next_text(self):
        return input()

    def get_async_command(self):
        if self.async_command is None:
            if self.thread is None:
                self.thread = threading.Thread(target=self.__thread_get_input, args=())
                self.thread.start()
            return_value = None
        else:
            return_value = self.async_command
            self.async_command = None
            self.thread = None
        return CommandFactory().get_command(return_value)

    def __thread_get_input(self):
        self.async_command = input()
