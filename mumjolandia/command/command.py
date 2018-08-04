from enum import Enum


class Type(Enum):
    type = 1
    type2 = 2


class Command:
    def __init__(self, name):
        self.name = name
        self.arguments = []

