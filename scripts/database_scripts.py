from src.interface.food.recipe_day import RecipeDay
from src.modules.food.food_database_helper import FoodDatabaseHelper
from src.modules.food.food_supervisor import FoodSupervisor
from src.modules.food.utils.meal_loader_from_file import MealLoaderFromFile


db_location = '../data/jedzonko.db'
meal_data_location = 'meal_data.txt'


def get_recipe(id_recipe=1):
    s = FoodSupervisor(db_location)
    x = s.get_recipe_day(id_recipe)
    return x


def get_recipes_ids():
    return_value = []
    h = FoodDatabaseHelper(db_location)
    for x in h.get_recipes_ids():
        return_value.append(x[0])
    return return_value


def add_meals_from_file(meal_type=None):
    m = MealLoaderFromFile(meal_data_location)
    x = m.load_meals(meal_type)
    s = FoodSupervisor(db_location)
    if meal_type is None:
        r = RecipeDay(x[0], x[1], x[2], x[3], x[4])
        s.add_recipe_day(r)
    else:
        for meal in x:
            s.insert_meal(meal)
