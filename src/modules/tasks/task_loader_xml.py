import xml.etree.ElementTree as ET
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_file_broken_exception import TaskFileBrokenException
from src.modules.tasks.task_priority import TaskPriority


class TaskLoader:
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
                name = 'error'
                # tag = child.tag
                name = child.get('name')
                date = child.get('date')
                priority = child.get('priority')
                if name is None:
                    broken_file_flag = True
                    name = 'error'
                # print(tag)
                # print(attrib)
                tasks.append(self.task_factory.get_task(name, priority, date))
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
            ET.SubElement(root_element, "task", name=t.text, date=str(t.date), priority=str(t.priority)).text = "none"
        tree = ET.ElementTree(root_element)
        tree.write(self.task_file)
