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
        return 1

    def execute(self, command):
        command_length = len(command.arguments)
        if command_length == 0:
            print('Commands:')
            print('print, add x')
            return 0
        if command.arguments[0] == 'print':
            self.print()
            return 0
        elif command.arguments[0] == 'add':
            if command_length < 2:
                print('Task name not given')
                return 0
            else:
                if self.add_task(command.arguments[1]):
                    print('ok')
                    return 0
                return 1
        else:
            return 1
