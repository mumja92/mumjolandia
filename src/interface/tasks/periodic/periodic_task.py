from enum import Enum

import datetime

import logging

from src.interface.mumjolandia.pod_template import PODTemplate
from src.utils.helpers import DateHelper


class PeriodicTaskOccurrenceType(Enum):
    day = 1,
    week = 2,
    year = 3,


class PeriodicTask(PODTemplate):
    def __init__(self,
                 name,
                 occurrence_type,
                 occurrence,
                 reminder,
                 start,
                 task_type,
                 ):
        self.name = name
        self.occurrence_type = occurrence_type
        self.occurrence = occurrence
        self.reminder = reminder
        self.start = start
        self.task_type = task_type

    def __str__(self):
        return self.name

    def is_to_be_reminded(self, date=DateHelper.get_today_short()):
        if isinstance(date, int):
            date = DateHelper.get_today_short(date)
        next_occurrence = self.get_next_occurrence_in_days_as_int(date)
        if next_occurrence <= self.reminder:
            return True
        return False

    def get_next_occurrence_in_days_as_int(self, date=0):
        # todo: add tests to check that int parameter works correctly
        return_value = None
        if isinstance(date, int):
            date = DateHelper.get_today_short(date)
        if not isinstance(date, datetime.date):
            logging.error("Date parameter type is not datetime.Date")
            return None
        if self.occurrence_type is PeriodicTaskOccurrenceType.year:
            delta_days = (self.start - date).days
            return delta_days
        else:
            wheel_date = self.start
            wheel_amount = self.occurrence
            if self.occurrence_type is PeriodicTaskOccurrenceType.day:
                pass
            if self.occurrence_type is PeriodicTaskOccurrenceType.week:
                wheel_amount *= 7
            while wheel_date < date:
                wheel_date += datetime.timedelta(wheel_amount)
            return_value = (wheel_date - date).days
        return return_value

    def get_next_occurrence_as_date(self, date=0):
        return DateHelper.get_today_short(self.get_next_occurrence_in_days_as_int(date))
