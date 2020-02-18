import datetime


class DateTimeHelper:
    fixed_date_today = datetime.datetime(2018, 4, 13)

    @staticmethod
    def get_fixed_datetime(day_amount=0):
        return DateTimeHelper.fixed_date_today + datetime.timedelta(days=day_amount)

    @staticmethod
    def get_fixed_date(day_amount=0):
        return (DateTimeHelper.fixed_date_today + datetime.timedelta(days=day_amount)).date()
