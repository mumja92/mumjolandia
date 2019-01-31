from enum import Enum


class TaskType(Enum):
    unknown = 0
    normal = 1
    should_have = 2
    periodic = 3
