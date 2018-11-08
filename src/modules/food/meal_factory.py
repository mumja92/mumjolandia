from src.interface.food.food_sql_enums import MealType
from src.interface.food.meal import Meal


class MealFactory:
    def get_meal(self, name, recipe, meal_type, ingredients):
        return Meal(name, recipe, meal_type, ingredients)

    def get_meal_breakfast(self, name, recipe, ingredients):
        return Meal(name, recipe, MealType.breakfast.value, ingredients)

    def get_meal_second_breakfast(self, name, recipe, ingredients):
        return Meal(name, recipe, MealType.second_breakfast.value, ingredients)

    def get_meal_dinner(self, name, recipe, ingredients):
        return Meal(name, recipe, MealType.dinner.value, ingredients)

    def get_meal_tea(self, name, recipe, ingredients):
        return Meal(name, recipe, MealType.tea.value, ingredients)

    def get_meal_supper(self, name, recipe, ingredients):
        return Meal(name, recipe, MealType.supper.value, ingredients)

