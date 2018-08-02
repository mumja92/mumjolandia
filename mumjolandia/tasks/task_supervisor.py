from mumjolandia.tasks.task import Task
from mumjolandia.tasks.task_loader import TaskLoader


class TaskSupervisor:
    def __init__(self):
        self.task_loader = TaskLoader("tasks.xml")
        self.tasks = self.task_loader.get_tasks()

    def __del__(self):
        self.task_loader.save_tasks(self.tasks)

    def print(self):
        for t in self.tasks:
            print(t.text)

    def add_task(self, name):
        self.tasks.append(Task(name))
