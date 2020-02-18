from src.utils.helpers import DateHelper


class TaskReminder:
    @staticmethod
    def should_be_reminded(task, date=DateHelper.get_today_short()):
        diff = task.date_to_finish - date
        if diff.days <= task.reminder:
            return True
        return False
