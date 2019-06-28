from enum import Enum


class MumjolandiaConfigBool(Enum):
    true = 0
    false = 1


class MumjolandiaLogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5
