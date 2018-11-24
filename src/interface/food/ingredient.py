from src.interface.food.food_sql_enums import AmountType
from src.interface.mumjolandia.pod_template import PODTemplate


class Ingredient(PODTemplate):
    def __init__(self, name, amount, amount_type):
        self.name = name
        self.amount = amount
        self.amount_type = amount_type

    def __str__(self):
        if self.amount_type == AmountType['a_little']:
            return self.name + ": a little"
        else:
            return self.name + ": " + str(self.amount) + " [" + self.amount_type.name + "]"
