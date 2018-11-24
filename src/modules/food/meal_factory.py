from src.interface.food.food_sql_enums import MealType
from src.interface.food.meal import Meal


class MealFactory:
    @staticmethod
    def get_meal(name=None, recipe=None, meal_type=None, ingredients=None):
        if meal_type is MealType:
            return Meal(name, recipe, meal_type, ingredients)
        else:
            return Meal(name, recipe, MealType(meal_type), ingredients)
