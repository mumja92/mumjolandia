# from PySide2.QtWidgets import QApplication, QLabel


class MumjolandiaGui:
    def __init__(self, queue):
        self.queue = queue

    def run(self):
        pass
        # app = QApplication([])
        # label = QLabel("Hello Qt for Python!")
        # label.show()
        # app.exec_()

    def __pass_command(self, command):
        self.queue.put(command)
