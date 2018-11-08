from src.interface.food.food_sql_enums import AmountType
from src.interface.food.ingredient import Ingredient


class IngredientFactory:
    def get_ingredient_g(self, name, amount):
        return Ingredient(name, amount, AmountType.g.value)

    def get_ingredient_number(self, name, amount):
        return Ingredient(name, amount, AmountType.number.value)

    def get_ingredient_a_little(self, name, amount):
        return Ingredient(name, amount, AmountType.a_little.value)

    def get_ingredient_ml(self, name, amount):
        return Ingredient(name, amount, AmountType.ml.value)
