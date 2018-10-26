class MumjolandiaDataPasser:
    def __init__(self, supervisors, queue):
        self.supervisors = supervisors
        self.queue = queue

    def get_tasks(self):
        return self.supervisors['task'].get_tasks()

    def pass_command(self, command):
        self.queue.put(command)
