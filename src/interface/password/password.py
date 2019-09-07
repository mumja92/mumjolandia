class Password:
    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password

    def __str__(self):
        return str(self.password)
