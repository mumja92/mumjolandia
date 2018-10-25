from enum import Enum


class TaskOccurrence(Enum):
    unknown = 0
    once = 1
    every_week = 2
    every_day = 3
    other = 4
