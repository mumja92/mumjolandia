from threading import Thread

import logging


class ThreadWatcher:
    def __init__(self, threads):
        self.threads = threads
        if not isinstance(self.threads, list) and self.threads is not None:
            logging.error("Wrong type passed to constructor: " + self.threads.__class__.__name__)
            self.threads = []
        for thread in reversed(self.threads):
            if not isinstance(thread, Thread):
                logging.error("Passed thread is not 'Thread' type! Type: " + thread.__class__.__name__)
                self.threads.pop(thread)

    def join(self):
        all_threads_ok = True
        for thread in reversed(self.threads):
            if not self.__check_thread_alive(thread):
                all_threads_ok = False
                self.threads.pop(thread)
                logging.critical("Thread " + thread.getName() + " crashed")
        if not all_threads_ok:
            pass

    def __check_thread_alive(self, thread):
        return True
