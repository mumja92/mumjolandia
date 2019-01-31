from src.interface.mumjolandia.pod_template import PODTemplate
from src.interface.tasks.task_status import TaskStatus


class Task(PODTemplate):
    def __init__(self, name, description, date_added, date_to_finish, priority, task_type, status):
        self.name = name
        self.description = description
        self.date_added = date_added
        self.date_to_finish = date_to_finish
        self.priority = priority
        self.type = task_type
        self.status = status

    def __str__(self):
        status = 'error'
        if self.status == TaskStatus.done:
            status = '+'
        if self.status == TaskStatus.not_done:
            status = '-'
        if self.status == TaskStatus.unknown:
            status = '?'
        return '[' + status + '] ' + self.name + ' - ' + str(self.date_to_finish)
