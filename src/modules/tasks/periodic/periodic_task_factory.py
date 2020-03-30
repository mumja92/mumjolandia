import datetime
import logging

from src.interface.tasks.periodic.periodic_task import PeriodicTaskOccurrenceType, PeriodicTask
from src.utils.helpers import DateHelper


class PeriodicTaskFactory:
    @staticmethod
    def get_periodic_task(name='unknown',
                          occurrence_type=PeriodicTaskOccurrenceType.day,
                          occurrence=1,
                          reminder=0,
                          start=None,
                          ):
        if start is None:
            start = DateHelper.get_today_short()
        try:
            if isinstance(start, str):
                start = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        except ValueError as e:
            logging.error("Conversion error: " + str(e))
            return None
        return PeriodicTask(name, occurrence_type, int(occurrence), int(reminder), start)
