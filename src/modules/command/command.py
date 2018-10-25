class Command:
    def __init__(self, arguments):
        self.arguments = arguments

    def __str__(self):
        return str(self.arguments)
