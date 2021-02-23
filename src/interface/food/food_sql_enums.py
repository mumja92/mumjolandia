from enum import Enum


class AmountType(Enum):
    error = 0
    g = 1
    number = 2
    a_little = 3
    ml = 4
    handful = 5
    slice = 6
    spoon = 7
    cm = 8


class MealType(Enum):
    breakfast = 1
    second_breakfast = 2
    dinner = 3
    tea = 4
    supper = 5
