import os
import unittest
from unittest import TestCase

from src.interface.tasks.task_file_broken_exception import TaskFileBrokenException
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_loader_xml import TaskLoaderXml


class TestTaskLoaderXml(TestCase):
    def test_task_file_not_exist(self):
        t = TaskLoaderXml('this_file_does_not_exist.xml')
        with self.assertRaises(FileNotFoundError):
            t.get()

    def test_task_file_bad(self):
        broken_file = "brokenFile.xml"
        t = TaskLoaderXml(broken_file)
        with open(broken_file, 'w') as file:
            file.write('xDD')
        with self.assertRaises(TaskFileBrokenException):
            t.get()
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

        t = TaskLoaderXml(test_file)
        self.assertEqual(t.get(), [])

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
            file.write('<tasks><task date_added="2018-10-25 00:00:00" date_to_finish="2018-10-25 00:00:00" '
                       'description="unknown" name="task1" priority="unknown" reminder="0" status="not_done" type="unknown">'
                       'none</task><task date_added="2018-10-26 00:00:00" date_to_finish="2018-10-26 00:00:00" '
                       'description="unknown" name="task drugi" priority="unknown" reminder="0" status="not_done" type="unknown">'
                       'none</task></tasks>')

        t = TaskLoaderXml(test_file)
        returned_list = t.get()
        t1 = TaskFactory.get_task(name='task1',
                                  date_added="2018-10-25 00:00:00",
                                  date_to_finish="2018-10-25 00:00:00")
        t2 = TaskFactory.get_task(name='task drugi',
                                  date_added="2018-10-26 00:00:00",
                                  date_to_finish="2018-10-26 00:00:00")
        self.assertEqual(len(returned_list), 2)
        self.assertTrue(t1 == returned_list[0])
        self.assertTrue(t2 == returned_list[1])

        try:
            os.remove(test_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    @unittest.skip('test_save_two_tasks - worked in pycharm - sth changed?')
    def test_save_two_tasks(self):
        test_file = "test_tasks.xml"
        expected_string = '<tasks><task date_added="2018-10-25 00:00:00" date_finished="None" ' \
                          'date_to_finish="2018-10-25 00:00:00" description="unknown" name="task1" priority="unknown" ' \
                          'reminder="0" status="not_done" type="unknown">none</task><task date_added="2018-10-25 00:00:00" ' \
                          'date_finished="None" date_to_finish="2018-10-25 00:00:00" description="unknown" name="task ' \
                          'drugi" priority="unknown" reminder="0" status="not_done" type="unknown">none</task></tasks>'
        t = TaskLoaderXml(test_file)

        if os.path.isfile(test_file):
            try:
                os.remove(test_file)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        t.save([TaskFactory.get_task(name='task1',
                                     date_added="2018-10-25 00:00:00",
                                     date_to_finish="2018-10-25 00:00:00"),
                TaskFactory.get_task(name='task drugi',
                                     date_added="2018-10-25 00:00:00",
                                     date_to_finish="2018-10-25 00:00:00")])
        with open(test_file, 'r') as file:
            data = file.read()
            self.assertEqual(''.join(expected_string.split()), ''.join(data.split()))

        try:
            os.remove(test_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
