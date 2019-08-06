from src.interface.mumjolandia.pod_template import PODTemplate


class MumjolandiaConfigObject(PODTemplate):
    def __init__(self,
                 log_level,
                 log_to_display,
                 log_to_file,
                 task_io_method,
                 server_address,
                 server_port,
                 shared_preferences_location):
        self.log_level = log_level
        self.log_to_display = log_to_display
        self.log_to_file = log_to_file
        self.task_io_method = task_io_method
        self.server_address = server_address
        self.server_port = server_port
        self.shared_preferences_location = shared_preferences_location
