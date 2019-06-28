from src.interface.mumjolandia.pod_template import PODTemplate


class MumjolandiaConfigObject(PODTemplate):
    def __init__(self, log_level, task_io_method):
        self.log_level = log_level
        self.task_io_method = task_io_method
