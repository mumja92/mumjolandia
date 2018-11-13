from src.interface.food.food_sql_enums import AmountType
from src.interface.food.ingredient import Ingredient


class IngredientFactory:
    @staticmethod
    def get_ingredient(name=None, amount=None, amount_type=None):
        a_type = amount_type
        if a_type is not None and a_type is not AmountType:
            try:
                a_type = AmountType(int(amount_type))
            except ValueError:
                a_type = AmountType['error']
        am = 0
        if amount is not None:
            try:
                am = int(amount)
            except ValueError:
                am = -1
        na = 'error'
        if name is not None:
            if len(name) > 0:
                na = name
        return Ingredient(na, am, a_type)

    @staticmethod
    def get_ingredient_g(name, amount):
        return Ingredient(name, amount, AmountType.g.value)

    @staticmethod
    def get_ingredient_number(name, amount):
        return Ingredient(name, amount, AmountType.number.value)

    @staticmethod
    def get_ingredient_a_little(name, amount):
        return Ingredient(name, amount, AmountType.a_little.value)

    @staticmethod
    def get_ingredient_ml(name, amount):
        return Ingredient(name, amount, AmountType.ml.value)
