import pickle
from src.modules.tasks.task_factory import TaskFactory


class TaskLoaderPickle:
    def __init__(self, task_file_name):
        self.task_file = task_file_name
        self.task_factory = TaskFactory()

    def get_tasks(self):
        tasks = []
        try:
            with open(self.task_file, 'rb') as fi:
                tasks = pickle.load(fi)
        except FileNotFoundError:
            pass
        return tasks

    def save_tasks(self, tasks):
        with open(self.task_file, 'wb') as fi:
            pickle.dump(tasks, fi)
