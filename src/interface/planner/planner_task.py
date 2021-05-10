from src.interface.mumjolandia.pod_template import PODTemplate


class PlannerTask(PODTemplate):
    def __init__(self, time: str, duration_minutes: int, description: str):
        self.time = time
        self.duration = duration_minutes
        self.description = description
