class MumjolandiaImmutableTypeWrapper:
    def __init__(self, item):
        self.object = item

    def change(self, value):
        self.object = value
