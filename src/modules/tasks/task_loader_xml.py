import xml.etree.ElementTree as ET

import datetime

from src.interface.tasks.task_file_broken_exception import TaskFileBrokenException
from src.interface.tasks.task_occurrence import TaskOccurrence
from src.interface.tasks.task_priority import TaskPriority
from src.interface.tasks.task_type import TaskType
from src.modules.tasks.task_factory import TaskFactory


class TaskLoaderXml:
    def __init__(self, task_file_name):
        self.task_file = task_file_name
        self.task_factory = TaskFactory()

    def get_tasks(self):
        tasks = []
        broken_file_flag = False
        try:
            tree = ET.parse(self.task_file)
            root_element = tree.getroot()
            for child in root_element:
                name = child.get('name')
                description = child.get('description')
                date_added = datetime.datetime.strptime(child.get('date_added'), '%Y-%m-%d %H:%M:%S')
                date_to_finish = datetime.datetime.strptime(child.get('date_to_finish'), '%Y-%m-%d %H:%M:%S')
                priority = TaskPriority[child.get('priority')]
                task_type = TaskType[child.get('type')]
                occurrence = TaskOccurrence[child.get('occurrence')]
                occurrence_list = child.get('occurrence_list')
                if name is None:
                    broken_file_flag = True
                    name = 'error'
                if description is None:
                    broken_file_flag = True
                    description = 'error'
                if date_added is None:
                    broken_file_flag = True
                    date_added = 'error'
                if date_to_finish is None:
                    broken_file_flag = True
                    date_to_finish = 'error'
                if priority is None:
                    broken_file_flag = True
                    priority = TaskPriority.unknown
                if task_type is None:
                    broken_file_flag = True
                    task_type = TaskType.unknown
                if occurrence is None:
                    broken_file_flag = True
                    occurrence = TaskOccurrence.unknown
                tasks.append(self.task_factory.get_task(name, description, date_added, date_to_finish, priority,
                                                        task_type, occurrence, occurrence_list))
        except FileNotFoundError:
            raise FileNotFoundError
        except ET.ParseError:
            raise TaskFileBrokenException(tasks)
        if broken_file_flag:
            raise TaskFileBrokenException(tasks)
        return tasks

    def save_tasks(self, tasks):
        root_element = ET.Element("tasks")
        for t in tasks:
            ET.SubElement(root_element,
                          "task",
                          name=t.name,
                          description=t.description,
                          date_added=t.date_added.strftime("%Y-%m-%d %H:%M:%S"),
                          date_to_finish=t.date_to_finish.strftime("%Y-%m-%d %H:%M:%S"),
                          priority=str(t.priority.name),
                          type=str(t.type.name),
                          occurrence=str(t.occurrence.name),
                          occurrence_list=str(t.occurrence_list)
                          ).text = "none"

        tree = ET.ElementTree(root_element)
        tree.write(self.task_file)
