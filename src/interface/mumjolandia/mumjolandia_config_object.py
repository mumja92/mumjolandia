from src.interface.mumjolandia.pod_template import PODTemplate


class MumjolandiaConfigObject(PODTemplate):
    def __init__(self, log_level, log_to_display, task_io_method):
        self.log_level = log_level
        self.log_print_to_display = log_to_display
        self.task_io_method = task_io_method
