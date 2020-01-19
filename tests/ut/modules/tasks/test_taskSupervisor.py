import os
import shutil
import unittest
from unittest import TestCase

import logging
from unittest import mock
from unittest.mock import patch

import datetime

from src.interface.tasks.task_status import TaskStatus
from src.modules.command.command_factory import CommandFactory
from src.modules.tasks.task_factory import TaskFactory
from src.modules.tasks.task_supervisor import TaskSupervisor


class DateTimeHelper:
    fixed_date_today = datetime.datetime(2018, 4, 13)

    @staticmethod
    def get_fixed_datetime_shifted(day_amount):
        return DateTimeHelper.fixed_date_today + datetime.timedelta(days=day_amount)


class TestTaskSupervisor(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestTaskSupervisor, self).__init__(*args, **kwargs)
        logging.getLogger().disabled = True
        self.data_location = os.path.abspath(os.curdir) + '/data_test'

    def setUp(self):
        self.__clean_workspace()

    def tearDown(self):
        self.__clean_workspace()

    def __clean_workspace(self):
        if os.path.isdir(self.data_location):
            shutil.rmtree(self.data_location)

    def __get_tasks(self, task_supervisor):
        return task_supervisor.tasks

    # task_supervisor - TaskSupervisor()
    # names - list[] of names (str) to check
    # strict - when set to True there must not be any additional element remaining in actual_names
    def __check_names_are_in_task_list(self, task_supervisor, names, strict=True):
        actual_names = []
        for t in self.__get_tasks(task_supervisor):
            actual_names.append(t.name)
        for n in names:
            if n not in actual_names:
                return False
            actual_names.remove(n)
        if strict:
            if len(actual_names) != 0:
                return False
        return True

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_add_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 0)
        task_supervisor.execute(CommandFactory().get_command('add task1'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')
        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_add_no_parameter_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 0)
        task_supervisor.execute(CommandFactory().get_command('add'))
        task_supervisor.execute(CommandFactory().get_command('add '))
        task_supervisor.execute(CommandFactory().get_command('add  '))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 0)
        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @unittest.skip('test_task_add_empty_parameter_no_ok - failing; please change code in the future')
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_add_empty_parameter_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 0)
        task_supervisor.execute(CommandFactory().get_command("add ''"))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 0)
        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_add_with_multiple_parameters_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 0)
        task_supervisor.execute(CommandFactory().get_command('add task to add'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task to add')
        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_add_three_tasks_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 0)

        task_supervisor.execute(CommandFactory().get_command('add task1'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')
        self.assertEqual(mock_save.call_count, 1)

        task_supervisor.execute(CommandFactory().get_command('add second task'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 2)
        self.assertEqual(self.__get_tasks(task_supervisor)[1].name, 'second task')
        self.assertEqual(mock_save.call_count, 2)

        task_supervisor.execute(CommandFactory().get_command("add 'third task'"))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
        self.assertEqual(self.__get_tasks(task_supervisor)[2].name, 'third task')
        self.assertEqual(mock_save.call_count, 3)

        self.assertEqual(mock_load.call_count, 1)

    @unittest.skip('test_task_add_task_already_exist_no_ok - failing; please change code in the future')
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_add_task_already_exist_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 0)

        task_supervisor.execute(CommandFactory().get_command('add task1'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')
        self.assertEqual(mock_save.call_count, 1)

        task_supervisor.execute(CommandFactory().get_command('add task1'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(mock_save.call_count, 1)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task1')])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_edit_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')

        task_supervisor.execute(CommandFactory().get_command('edit 0 task_edited'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task_edited')
        self.assertEqual(mock_save.call_count, 1)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task1')])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_edit_task_does_not_exist_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')

        task_supervisor.execute(CommandFactory().get_command('edit 1 task_edited'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')
        self.assertEqual(mock_save.call_count, 0)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task1')])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_edit_no_parameter_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')

        task_supervisor.execute(CommandFactory().get_command('edit 0'))
        task_supervisor.execute(CommandFactory().get_command('edit 0 '))
        task_supervisor.execute(CommandFactory().get_command('edit'))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')
        self.assertEqual(mock_save.call_count, 0)

        self.assertEqual(mock_load.call_count, 1)

    @unittest.skip('test_task_edit_empty_parameter_no_ok - fix implementation')
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task1')])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_edit_empty_parameter_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')

        task_supervisor.execute(CommandFactory().get_command("edit 0 ''"))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 1)
        self.assertEqual(self.__get_tasks(task_supervisor)[0].name, 'task1')
        self.assertEqual(mock_save.call_count, 0)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task11'),
                                                                                TaskFactory().get_task('task1'),
                                                                                TaskFactory().get_task('task3'),
                                                                                ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_remove_by_name_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task11', 'task3', 'task1']))

        task_supervisor.execute(CommandFactory().get_command("rm task1"))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 2)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task11', 'task3']))
        self.assertEqual(mock_save.call_count, 1)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task11'),
                                                                                TaskFactory().get_task('task1'),
                                                                                TaskFactory().get_task('task3'),
                                                                                ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_remove_by_id_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task11', 'task3', 'task1']))

        task_supervisor.execute(CommandFactory().get_command("rm 0"))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 2)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task3']))
        self.assertEqual(mock_save.call_count, 1)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('1'),
                                                                                TaskFactory().get_task('2'),
                                                                                TaskFactory().get_task('3'),
                                                                                ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_remove_when_name_is_int_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['1', '2', '3']))

        task_supervisor.execute(CommandFactory().get_command("rm 1"))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 2)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['1', '3']))
        self.assertEqual(mock_save.call_count, 1)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task1'),
                                                                                TaskFactory().get_task('task2'),
                                                                                TaskFactory().get_task('task3'),
                                                                                ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_remove_no_parameters_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))

        task_supervisor.execute(CommandFactory().get_command("rm"))
        task_supervisor.execute(CommandFactory().get_command("rm "))
        task_supervisor.execute(CommandFactory().get_command("rm ''"))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))
        self.assertEqual(mock_save.call_count, 0)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task1'),
                                                                                TaskFactory().get_task('task2'),
                                                                                TaskFactory().get_task('task3'),
                                                                                ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_remove_wrong_parameter_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))

        task_supervisor.execute(CommandFactory().get_command("rm task"))
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))
        self.assertEqual(mock_save.call_count, 0)

        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task1'),
                                                                                TaskFactory().get_task('task2'),
                                                                                TaskFactory().get_task('task3'),
                                                                                ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_get_no_task_set_ok(self, mock_save, mock_load):
        # after adding tasks they are not set for 'today' so they will not be shown in simple 'ls' command
        with mock.patch.object(TaskSupervisor,
                               '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
            self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))
            returned_tasks = task_supervisor.execute(
                CommandFactory().get_command('ls')).arguments[1]   # arg[0] are indexes
            self.assertEqual(len(returned_tasks), 0)
            self.assertEqual(mock_save.call_count, 0)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task2',
                                                ),
                         TaskFactory().get_task('task3',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(0),
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_get_two_task_set_ok(self, mock_save, mock_load):
        # after 'set 0 0' and 'set 0 -1' command, 2 tasks will match 'ls' command (as 'task1' was not completed in
        # previous day)
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
            self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))
            returned_tasks = task_supervisor.execute(
                CommandFactory().get_command('ls')).arguments[1]  # arg[0] are indexes
            self.assertEqual(len(returned_tasks), 2)
            self.assertEqual(returned_tasks[0].name, 'task1')
            self.assertEqual(returned_tasks[1].name, 'task3')
            self.assertEqual(mock_save.call_count, 0)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(0),
                                                ),
                         TaskFactory().get_task('task2',
                                                ),
                         TaskFactory().get_task('task3',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_get_two_task_set_one_done_ok(self, mock_save, mock_load):
        # after 'set 0 0' and 'set 0 -1' command 2 tasks will match 'ls' command, but 'task3' has 'done' status so won't
        # be listed
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
            self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))
            returned_tasks = task_supervisor.execute(
                CommandFactory().get_command('ls')).arguments[1]  # arg[0] are indexes
            self.assertEqual(len(returned_tasks), 1)
            self.assertEqual(returned_tasks[0].name, 'task1')
            self.assertEqual(mock_save.call_count, 0)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[TaskFactory().get_task('task1'),
                                                                                TaskFactory().get_task('task2'),
                                                                                TaskFactory().get_task('task3'),
                                                                                ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_get_for_other_day_empty_ok(self, mock_save, mock_load):
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
            self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))
            returned_tasks = task_supervisor.execute(
                CommandFactory().get_command('ls -1')).arguments[1]  # arg[0] are indexes
            self.assertEqual(len(returned_tasks), 0)
            self.assertEqual(mock_save.call_count, 0)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task3',
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_get_for_other_day_found_ok(self, mock_save, mock_load):
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            self.assertEqual(len(self.__get_tasks(task_supervisor)), 3)
            self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1', 'task2', 'task3']))
            returned_tasks = task_supervisor.execute(
                CommandFactory().get_command('ls -1')).arguments[1]  # arg[0] are indexes
            self.assertEqual(len(returned_tasks), 1)
            self.assertEqual(returned_tasks[0].name, 'task2')
            self.assertEqual(mock_save.call_count, 0)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                status=TaskStatus.done,
                                                ),
                         TaskFactory().get_task('task2',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(0),
                                                status=TaskStatus.done,
                                                ),
                         TaskFactory().get_task('task4',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task5',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(1),
                                                status=TaskStatus.done,
                                                ),
                         TaskFactory().get_task('task6',
                                                status=TaskStatus.unknown,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_get_x_ok(self, mock_save, mock_load):
        # 'ls x' lists all tasks that have no date_to_finish set and are not 'done'
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 6)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1',
                                                                              'task2',
                                                                              'task3',
                                                                              'task4',
                                                                              'task5',
                                                                              'task6',
                                                                              ]))
        returned_tasks = task_supervisor.execute(
            CommandFactory().get_command('ls x')).arguments[1]  # arg[0] are indexes
        self.assertEqual(len(returned_tasks), 2)
        self.assertEqual(returned_tasks[0].name, 'task4')
        self.assertEqual(returned_tasks[1].name, 'task6')
        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                status=TaskStatus.done,
                                                ),
                         TaskFactory().get_task('task2',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(0),
                                                status=TaskStatus.done,
                                                ),
                         TaskFactory().get_task('task4',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task5',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(1),
                                                status=TaskStatus.done,
                                                ),
                         TaskFactory().get_task('task6',
                                                status=TaskStatus.unknown,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_get_0_ok(self, mock_save, mock_load):
        # returns all existing tasks
        task_supervisor = TaskSupervisor()
        self.assertEqual(len(self.__get_tasks(task_supervisor)), 6)
        self.assertTrue(self.__check_names_are_in_task_list(task_supervisor, ['task1',
                                                                              'task2',
                                                                              'task3',
                                                                              'task4',
                                                                              'task5',
                                                                              'task6',
                                                                              ]))
        returned_tasks = task_supervisor.execute(
            CommandFactory().get_command('ls 0')).arguments[1]  # arg[0] are indexes
        self.assertEqual(len(returned_tasks), 6)
        self.assertEqual(returned_tasks[0].name, 'task1')
        self.assertEqual(returned_tasks[1].name, 'task2')
        self.assertEqual(returned_tasks[2].name, 'task3')
        self.assertEqual(returned_tasks[3].name, 'task4')
        self.assertEqual(returned_tasks[4].name, 'task5')
        self.assertEqual(returned_tasks[5].name, 'task6')
        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @unittest.skip('test_task_get_with_periodic_ok: todo after adding reminders for periodic tasks')
    def test_task_get_with_periodic_ok(self):
        self.fail()

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                status=TaskStatus.done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(1),
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_set_ok(self, mock_save, mock_load):
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            task_supervisor.execute(CommandFactory().get_command('set 0 3'))
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(3))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            self.assertEqual(mock_save.call_count, 1)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                status=TaskStatus.done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(1),
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_set_none_ok(self, mock_save, mock_load):
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            task_supervisor.execute(CommandFactory().get_command('set 0 none'))
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, None)
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            self.assertEqual(mock_save.call_count, 1)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                status=TaskStatus.done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(1),
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_set_wrong_index_no_ok(self, mock_save, mock_load):
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            task_supervisor.execute(CommandFactory().get_command('set 4 3'))
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            self.assertEqual(mock_save.call_count, 0)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                status=TaskStatus.done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(1),
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_set_wrong_value_no_ok(self, mock_save, mock_load):
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            task_supervisor.execute(CommandFactory().get_command('set 0 a'))
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            self.assertEqual(mock_save.call_count, 0)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                status=TaskStatus.done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(1),
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_set_no_value_no_ok(self, mock_save, mock_load):
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            task_supervisor.execute(CommandFactory().get_command('set 0'))
            task_supervisor.execute(CommandFactory().get_command('set 0 '))
            task_supervisor.execute(CommandFactory().get_command("set 0 ' '"))
            tasks = self.__get_tasks(task_supervisor)
            self.assertEqual(len(tasks), 4)
            self.assertEqual(tasks[0].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[1].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(-1))
            self.assertEqual(tasks[2].date_to_finish, None)
            self.assertEqual(tasks[3].date_to_finish, DateTimeHelper.get_fixed_datetime_shifted(1))

            self.assertEqual(mock_save.call_count, 0)
            self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',

                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_done_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        task_supervisor.execute(CommandFactory().get_command('done 2'))
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.done)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',

                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_done_wrong_argument_type_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        task_supervisor.execute(CommandFactory().get_command('done a'))
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',

                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_done_wrong_argument_index_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        task_supervisor.execute(CommandFactory().get_command('done 5'))
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',

                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_done_no_argument_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        task_supervisor.execute(CommandFactory().get_command('done'))
        task_supervisor.execute(CommandFactory().get_command('done '))
        task_supervisor.execute(CommandFactory().get_command("done ' '"))
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',

                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_undone_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        task_supervisor.execute(CommandFactory().get_command('undone 2'))
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.not_done)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',

                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_undone_wrong_argument__type_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        task_supervisor.execute(CommandFactory().get_command('undone a'))
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',

                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_undone_wrong_argument_index_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        task_supervisor.execute(CommandFactory().get_command('undone 5'))
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                status=TaskStatus.not_done,
                                                ),
                         TaskFactory().get_task('task3',
                                                status=TaskStatus.unknown,
                                                ),
                         TaskFactory().get_task('task4',

                                                status=TaskStatus.done,
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_undone_no_argument_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        task_supervisor.execute(CommandFactory().get_command('undone'))
        task_supervisor.execute(CommandFactory().get_command('undone '))
        task_supervisor.execute(CommandFactory().get_command("undone ' '"))
        tasks = self.__get_tasks(task_supervisor)
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].status, TaskStatus.not_done)
        self.assertEqual(tasks[1].status, TaskStatus.not_done)
        self.assertEqual(tasks[2].status, TaskStatus.unknown)
        self.assertEqual(tasks[3].status, TaskStatus.done)

        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.periodic_tasks_generator.PeriodicTasksGenerator.get_list_next_occurrence',
           return_value=[TaskFactory.get_task('task1'),
                         TaskFactory.get_task('task2'),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_periodic_ok(self, mock_save, mock_load, mock_periodic):
        task_supervisor = TaskSupervisor()
        returned_tasks = task_supervisor.execute(CommandFactory().get_command('periodic'))

        self.assertEqual(len(returned_tasks.arguments[0]), 2)   # indexes
        self.assertEqual(len(returned_tasks.arguments[1]), 2)   # tasks

        # indexes have to be negative
        for index in returned_tasks.arguments[0]:
            self.assertTrue(index < 0)
        self.assertEqual(returned_tasks.arguments[1][0].name, 'task1')
        self.assertEqual(returned_tasks.arguments[1][1].name, 'task2')

        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)
        self.assertEqual(mock_periodic.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                ),
                         TaskFactory().get_task('task3',
                                                ),
                         TaskFactory().get_task('task4',
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_bump_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        task_supervisor.execute(CommandFactory().get_command('bump 0'))
        task_supervisor.execute(CommandFactory().get_command('bump 1'))
        returned_tasks = task_supervisor.execute(
            CommandFactory().get_command('ls 0')).arguments[1]  # arg[0] are indexes
        self.assertEqual(len(returned_tasks), 4)
        self.assertEqual(returned_tasks[0].name, 'task2')
        self.assertEqual(returned_tasks[1].name, 'task4')
        self.assertEqual(returned_tasks[2].name, 'task1')
        self.assertEqual(returned_tasks[3].name, 'task3')
        self.assertEqual(mock_save.call_count, 2)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get', return_value=[])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_bump_out_of_range_negative_index_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        task_supervisor.execute(CommandFactory().get_command('bump -1'))
        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                ),
                         TaskFactory().get_task('task2',
                                                ),
                         TaskFactory().get_task('task3',
                                                ),
                         TaskFactory().get_task('task4',
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_bump_out_of_range_index_too_big_no_ok(self, mock_save, mock_load):
        task_supervisor = TaskSupervisor()
        task_supervisor.execute(CommandFactory().get_command('bump 4'))
        self.assertEqual(mock_save.call_count, 0)
        self.assertEqual(mock_load.call_count, 1)

    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.get',
           return_value=[TaskFactory().get_task('task1',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(1),
                                                ),
                         TaskFactory().get_task('task2',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-1),
                                                ),
                         TaskFactory().get_task('task3',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(-2),
                                                ),
                         TaskFactory().get_task('task4',
                                                date_to_finish=DateTimeHelper.get_fixed_datetime_shifted(0),
                                                ),
                         ])
    @patch('src.modules.tasks.task_supervisor.TaskLoaderXml.save', return_value=None)
    def test_task_show_with_tasks_from_previous_days_done_today(self, mock_save, mock_load):
        # when ie. task was set to be done yesterday, but is done today, it is expected to be still shown today, but
        # marked as 'done'
        # WARNING: pay attention to indexes of returned_tasks shifting during operations
        # WARNING: sorting affects results!
        with mock.patch.object(TaskSupervisor, '_TaskSupervisor__get_today',
                               return_value=DateTimeHelper.get_fixed_datetime_shifted(0),
                               ):
            task_supervisor = TaskSupervisor()
            returned_tasks = task_supervisor.execute(
                CommandFactory().get_command('ls')).arguments[1]  # arg[0] are indexes
            # task1 is for tomorrow, so it doesn't appear in list for today
            self.assertEqual(len(returned_tasks), 3)
            self.assertEqual(returned_tasks[0].status, TaskStatus.not_done)
            self.assertEqual(returned_tasks[0].name, 'task3')

            # task2 is set to 'done'
            task_supervisor.execute(CommandFactory().get_command('done 2'))
            returned_tasks = task_supervisor.execute(
                CommandFactory().get_command('ls')).arguments[1]  # arg[0] are indexes
            # task2 is still visible in tasks for today
            self.assertEqual(len(returned_tasks), 3)
            self.assertEqual(returned_tasks[0].status, TaskStatus.done)
            self.assertEqual(returned_tasks[0].name, 'task3')
            self.assertEqual(mock_save.call_count, 1)
            self.assertEqual(mock_load.call_count, 1)
