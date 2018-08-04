from mumjolandia.console.console import Console
from mumjolandia.tasks.task_supervisor import TaskSupervisor


class Mumjolandia:
    def __init__(self):
        self.console = Console()
        self.taskSupervisor = TaskSupervisor()
        self.mode = 1  # dont need to type first word for command

    def run(self):
        while True:
            command = self.console.get_next_command()
            if command.name == 'xD':
                self.taskSupervisor.print()
            elif command.name == 'exit':
                break
            else:
                self.taskSupervisor.add_task(command.name)
                # print(command)
