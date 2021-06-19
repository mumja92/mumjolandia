import logging

from src.interface.mumjolandia.pod_template import PODTemplate
from src.interface.planner.planner_task import PlannerTask
from src.modules.planner.planner_task_factory import PlannerTaskFactory
from src.utils.helpers import DateHelper


class Plan(PODTemplate):
    def __init__(self, date_shift: int):
        self.date = DateHelper.get_today_short(date_shift)
        self.planner_tasks: [PlannerTask] = []

    def __str__(self):
        return_value = str(self.date) + "\n"
        return_value += "tasks:\n"
        for planner_task in self.planner_tasks:
            return_value += str(planner_task)
        return return_value

    def add_task(self, task_name: str, duration: int, task_date: str):
        planner_task = PlannerTaskFactory.get(task_date, duration, task_name)
        if planner_task is None:
            return False
        else:
            if self.__validate_task_time(planner_task.time, planner_task.duration):
                for task in self.planner_tasks:
                    if task.time == task_date:
                        return self.modify_task(task_name, duration, task_date)
                self.planner_tasks.append(planner_task)
                return True
            return False

    def modify_task(self, task_name: str, duration: int, task_date: str):
        for task in self.planner_tasks:
            if task.time == task_date:
                task.duration = duration
                task.description = task_name
                return True
        return False

    def remove_task(self, hour: str):
        for index, planner_task in enumerate(self.planner_tasks):
            if planner_task.time == hour:
                self.planner_tasks.remove(planner_task)
                return True
        return False

    def is_empty(self):
        return not bool(len(self.planner_tasks))

    def __get_task_index(self, time: str):
        current_index = 0
        for plannerTask in self.planner_tasks:
            if plannerTask.time == time:
                return current_index
            current_index += 1
        return None

    def __validate_task_time(self, time: str, duration: int):
        # get int time for easier calculations
        if time[0] == "0":
            new_hour = int(time[1])
        else:
            new_hour = int(time[0:2])
        if time[3] == "0":
            new_minute = int(time[4])
        else:
            new_minute = int(time[3:5])
        for existing_task in self.planner_tasks:
            if existing_task.time[0] == "0":
                existing_hour = int(existing_task.time[1])
            else:
                existing_hour = int(existing_task.time[0:2])
            if existing_task.time[3] == "0":
                existing_minute = int(existing_task.time[4])
            else:
                existing_minute = int(existing_task.time[3:5])
            if new_hour == existing_hour and new_minute == existing_minute:
                return False
            if new_hour > existing_hour or (new_hour == existing_hour and new_minute > existing_minute):
                # new task is after existing task
                free_hour = existing_hour
                free_minute = existing_minute + existing_task.duration
                while free_minute > 59:
                    free_hour += 1
                    free_minute -= 60
                if free_hour > new_hour or (free_hour == new_hour and free_minute > new_minute):
                    return False
            else:
                # new task is before existing task
                free_hour = new_hour
                free_minute = new_minute + duration
                while free_minute > 59:
                    free_hour += 1
                    free_minute -= 60
                if free_hour > existing_hour or (free_hour == existing_hour and free_minute > existing_minute):
                    return False
        return True
