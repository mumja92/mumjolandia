class Message:
    def __init__(self, status: int, data):
        self.data = data
        self.status = status

    # first 4 bytes are size
    # next 2 bytes are status
    def get(self):
        return len(self.data).to_bytes(4, byteorder='big', signed=False) + self.status.to_bytes(2, byteorder='big', signed=False) + self.data

    def get_string(self):
        return self.data.decode('utf-8')

    def get_raw(self):
        return self.data
