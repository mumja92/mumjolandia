class MumjolandiaDataPasser:
    def __init__(self, supervisors, queue_in, queue_response, mutex, event):
        self.supervisors = supervisors
        self.queue_in = queue_in
        self.queue_response = queue_response
        self.mutex = mutex
        self.event = event

    def get_tasks(self):
        return self.supervisors['task'].get_tasks()

    def pass_command(self, command):
        self.mutex.acquire()
        return_value = None
        try:
            self.queue_in.put(command)
            self.event.wait()
            self.event.clear()
            return_value = self.queue_response.get()
            self.queue_response.task_done()
        finally:
            self.mutex.release()
            return return_value
