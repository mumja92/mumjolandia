from mumjolandia.tasks.task import Task
import xml.etree.ElementTree as ET

from mumjolandia.tasks.task_factory import TaskFactory


class TaskLoader:
    def __init__(self, task_file_name):
        self.task_file = task_file_name
        self.task_factory = TaskFactory()

    def get_tasks(self):
        tasks = []
        try:
            tree = ET.parse(self.task_file)
            root_element = tree.getroot()
            for child in root_element:
                # tag = child.tag
                attrib = child.get('name')
                # print(tag)
                # print(attrib)
                tasks.append(self.task_factory.get_task(attrib))
        except FileNotFoundError:
            print('file not found')
        return tasks

    def save_tasks(self, tasks):
        root_element = ET.Element("tasks")
        for t in tasks:
            ET.SubElement(root_element, "task", name=t.text).text = "none"
        tree = ET.ElementTree(root_element)
        tree.write(self.task_file)
