from src.interface.mumjolandia.pod_template import PODTemplate


class Note(PODTemplate):
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text
