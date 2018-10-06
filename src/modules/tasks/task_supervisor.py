from src.modules.tasks.task import Task
from src.modules.tasks.task_file_broken_exception import TaskFileBrokenException
from src.modules.tasks.task_loader_xml import TaskLoader


class TaskSupervisor:
    def __init__(self):
        self.allowedToSaveTasks = True                      # if loaded tasks are broken they wont be overwritten to not loose them
        self.task_loader = TaskLoader("tasks.xml")
        try:
            self.tasks = self.task_loader.get_tasks()
        except FileNotFoundError:
            print('TaskSupervisor::constructor - file doesnt exist')
            self.tasks = []
        except TaskFileBrokenException as e:
            print('TaskSupervisor::constructor - file broken. Not saving changes!')
            self.tasks = e.args[0]
            self.allowedToSaveTasks = False

    def __del__(self):
        if self.allowedToSaveTasks:
            self.task_loader.save_tasks(self.tasks)

    def print(self):
        print(len(self.tasks), 'items:')
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
