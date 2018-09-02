from PySide2.QtWidgets import QApplication, QLabel


class MumjolandiaGui():
    def __init__(self, val):
        self.arg = val

    def run(self):
        app = QApplication([])
        label = QLabel("Hello Qt for Python!")
        label.show()
        app.exec_()

    def __pass_command(self, command):
        # todo: pass command to mumjolandia
        pass
