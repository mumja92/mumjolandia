from src.interface.mumjolandia.pod_template import PODTemplate


class Command(PODTemplate):
    def __init__(self, arguments):
        self.arguments = arguments

    def __str__(self):
        return str(self.arguments)
