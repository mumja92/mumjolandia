from mumjolandia.console.console import Console
from mumjolandia.tasks.task_supervisor import TaskSupervisor


class Mumjolandia:
    def __init__(self):
        self.console = Console()
        self.taskSupervisor = TaskSupervisor()

    def run(self):
        while True:
            command = self.console.get_next_command()
            if command == 'xD':
                self.taskSupervisor.print()
            elif command == 'exit':
                break
            else:
                self.taskSupervisor.add_task(command)
                # print(command)
