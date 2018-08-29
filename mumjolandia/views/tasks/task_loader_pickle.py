import pickle
from mumjolandia.views.tasks.task_factory import TaskFactory


class TaskLoader:
    def __init__(self, task_file_name):
        self.task_file = task_file_name
        self.task_factory = TaskFactory()

    def get_tasks(self):
        tasks = []
        newfile = 'tasks.pk'
        try:
            with open(newfile, 'rb') as fi:
                tasks = pickle.load(fi)
        except FileNotFoundError:
            pass
        return tasks

    def save_tasks(self, tasks):
        newfile = 'tasks.pk'
        with open(newfile, 'wb') as fi:
            pickle.dump(tasks, fi)
