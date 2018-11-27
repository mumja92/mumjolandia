from src.interface.mumjolandia.pod_template import PODTemplate


class Game(PODTemplate):
    def __init__(self, text, description):
        self.name = text
        self.description = description

    def __str__(self):
        return self.name + ' - ' + self.description
