class Message:
    def __init__(self, data):
        self.data = data

    # first 4 bytes are size
    def get(self):
        return len(self.data).to_bytes(4, byteorder='big', signed=False) + self.data

    def get_string(self):
        return self.data.decode('utf-8')

    def get_raw(self):
        return self.data
