from src.interface.mumjolandia.pod_template import PODTemplate


class Event(PODTemplate):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
