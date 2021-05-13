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
            if self.__validate_task_time(planner_task):
                self.planner_tasks.append(planner_task)
                return True
            return False

    def modify_task(self, task_name: str, duration: int, task_date: str):
        logging.warning("Not implemented")
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

    def __validate_task_time(self, task):
        # todo: implement checking if task can be added at this time
        return True
