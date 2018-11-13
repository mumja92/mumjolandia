from src.interface.food.food_sql_enums import MealType
from src.interface.food.meal import Meal


class MealFactory:
    @staticmethod
    def get_meal(name=None, recipe=None, meal_type=None, ingredients=None):
        return Meal(name, recipe, meal_type, ingredients)

    @staticmethod
    def get_meal_breakfast(name, recipe, ingredients):
        return Meal(name, recipe, MealType.breakfast.value, ingredients)

    @staticmethod
    def get_meal_second_breakfast(name, recipe, ingredients):
        return Meal(name, recipe, MealType.second_breakfast.value, ingredients)

    @staticmethod
    def get_meal_dinner(name, recipe, ingredients):
        return Meal(name, recipe, MealType.dinner.value, ingredients)

    @staticmethod
    def get_meal_tea(name, recipe, ingredients):
        return Meal(name, recipe, MealType.tea.value, ingredients)

    @staticmethod
    def get_meal_supper(name, recipe, ingredients):
        return Meal(name, recipe, MealType.supper.value, ingredients)

