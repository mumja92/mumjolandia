from src.interface.mumjolandia.pod_template import PODTemplate


class Fat(PODTemplate):
    def __init__(self, name, date_added):
        self.value = name
        self.date_added = date_added

    def __str__(self):
        return str(self.value) + ' - ' + str(self.date_added)
