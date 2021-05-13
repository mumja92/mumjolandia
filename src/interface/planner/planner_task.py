from src.interface.mumjolandia.pod_template import PODTemplate


class PlannerTask(PODTemplate):
    def __init__(self, time: str, duration_minutes: int, description: str):
        self.time = time
        self.duration = duration_minutes
        self.description = description

    def __str__(self):
        return_value = str(self.time) + "\n"
        return_value += str(self.duration) + "\n"
        return_value += str(self.description) + "\n"
        return return_value
