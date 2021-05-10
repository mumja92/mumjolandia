import logging

from src.interface.planner.planner_task import PlannerTask


class PlannerTaskFactory:
    @staticmethod
    def get(time: str, duration_minutes: int, description: str):
        if not PlannerTaskFactory.__validate_time(time):
            logging.warning("Incorrect time given: " + str(time))
            return None
        if duration_minutes < 0:
            logging.warning("duration can't be <-0: " + str(duration_minutes))
            return None
        return PlannerTask(time, duration_minutes, description)

    @staticmethod
    def __validate_time(time):
        try:
            if not isinstance(time, str):
                return False
            if len(time) is not 5:
                return False
            if time[2] != ':':
                return False
            if int(time[0]) > 2 or int(time[0]) < 0:
                return False
            int(time[1])
            if int(time[3]) > 5 or int(time[0]) < 0:
                return False
            int(time[4])
            return True
        except ValueError:  # int(time[x]) fails
            return False
