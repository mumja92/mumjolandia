from unittest import TestCase

from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_file_broken_exception import TaskFileBrokenException
from src.modules.tasks.task_loader_xml import TaskLoader
import os


class TestTaskLoaderXml(TestCase):

    def test_task_file_not_exist(self):
        t = TaskLoader('this_file_does_not_exist.xml')
        with self.assertRaises(FileNotFoundError):
            t.get_tasks()

    def test_task_file_bad(self):
        broken_file = "brokenFile.xml"
        t = TaskLoader(broken_file)
        with open(broken_file, 'w') as file:
            file.write('xDD')
        with self.assertRaises(TaskFileBrokenException):
            t.get_tasks()
        try:
            os.remove(broken_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def test_get_tasks_from_empty_file(self):
        test_file = "test_tasks.xml"
        if os.path.isfile(test_file):
            try:
                os.remove(test_file)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        with open(test_file, 'w') as file:
            file.write('<tasks />')

        t = TaskLoader(test_file)
        self.assertEquals(t.get_tasks(), [])

        try:
            os.remove(test_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def test_get_tasks_from_file_with_two_tasks(self):
        test_file = "test_tasks.xml"
        if os.path.isfile(test_file):
            try:
                os.remove(test_file)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
        with open(test_file, 'w') as file:
            file.write('<tasks><task name="task1">none</task><task name="task drugi">none</task></tasks>')

        t = TaskLoader(test_file)
        returned_list = t.get_tasks()
        self.assertEquals(len(returned_list), 2)
        self.assertEquals(returned_list[0].text, 'task1')
        self.assertEquals(returned_list[1].text, 'task drugi')

        try:
            os.remove(test_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def test_save_two_tasks(self):
        test_file = "test_tasks.xml"
        expected_string = '<tasks><task name="task1">none</task><task name="task drugi">none</task></tasks>'
        t = TaskLoader(test_file)

        if os.path.isfile(test_file):
            try:
                os.remove(test_file)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        t.save_tasks([TaskFactory.get_task('task1'), TaskFactory.get_task('task drugi')])
        with open(test_file, 'r') as file:
            data = file.read()
            self.assertEquals(expected_string, data)

        try:
            os.remove(test_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))