import datetime

from src.interface.mumjolandia.pod_template import PODTemplate


class Event(PODTemplate):
    def __init__(self, name, date):
        self.name = name
        self.date = date

    def __str__(self):
        return str(self.date.strftime('%d-%m')) + ': ' + self.name
