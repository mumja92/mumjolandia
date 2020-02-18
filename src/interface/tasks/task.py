from src.interface.mumjolandia.pod_template import PODTemplate
from src.interface.tasks.task_status import TaskStatus
from src.interface.tasks.task_type import TaskType


class Task(PODTemplate):
    def __init__(self,
                 name,
                 description,
                 date_added,
                 date_to_finish,
                 date_finished,
                 priority,
                 task_type,
                 status,
                 reminder,
                 ):
        self.name = name
        self.description = description
        self.date_added = date_added
        self.date_to_finish = date_to_finish
        self.date_finished = date_finished
        self.priority = priority
        self.type = task_type
        self.status = status
        self.reminder = reminder

    def __str__(self):
        status = 'error'
        if self.status == TaskStatus.done:
            status = '++'
        if self.status == TaskStatus.not_done:
            status = '--'
        if self.status == TaskStatus.unknown:
            status = '??'
        if self.type == TaskType.periodic:
            if self.status == TaskStatus.done:
                status = 'p+'
            else:
                status = 'p-'
        if self.date_to_finish is None:
            date_to_finish = '-'
        else:
            date_to_finish = str(self.date_to_finish.strftime('%d %b'))
        return '[' + status + ']' + '(' + date_to_finish + ') ' + self.name
