import xml.etree.ElementTree as ET
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_file_broken_exception import TaskFileBrokenException


class TaskLoader:
    def __init__(self, task_file_name):
        self.task_file = task_file_name
        self.task_factory = TaskFactory()

    def get_tasks(self):
        tasks = []
        brokenFileFlag = False
        try:
            tree = ET.parse(self.task_file)
            root_element = tree.getroot()
            for child in root_element:
                attrib = 'error'
                # tag = child.tag
                attrib = child.get('name')
                if attrib is None:
                    brokenFileFlag = True
                    attrib = 'error'
                # print(tag)
                # print(attrib)
                tasks.append(self.task_factory.get_task(attrib))
        except FileNotFoundError:
            raise FileNotFoundError
        except ET.ParseError:
            raise TaskFileBrokenException(tasks)
        if brokenFileFlag:
            raise TaskFileBrokenException(tasks)
        return tasks

    def save_tasks(self, tasks):
        root_element = ET.Element("tasks")
        for t in tasks:
            ET.SubElement(root_element, "task", name=t.text).text = "none"
        tree = ET.ElementTree(root_element)
        tree.write(self.task_file)
