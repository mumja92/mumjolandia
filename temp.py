# db browser for sqlite
import sqlite3

from src.interface.food.food_sql_enums import AmountType
from src.interface.food.recipe_day import RecipeDay
from src.modules.fat.fat_factory import FatFactory
from src.modules.food.food_database_helper import FoodDatabaseHelper
from src.modules.food.food_supervisor import FoodSupervisor
from src.modules.food.ingredient_factory import IngredientFactory
from src.modules.food.meal_factory import MealFactory
from src.modules.food.utils.meal_loader_from_file import MealLoaderFromFile
from src.utils.polish_utf_to_ascii import PolishUtfToAscii

db_location = 'data/jedzonko.db'


def xml_to_dict():
    from src.utils import xmltodict
    with open('data/tasks.xml', 'r') as my_file:
        data = my_file.read()
    a = xmltodict.parse(data)
    pass
    for i in a['tasks']['task']:
        print('name: ' + i['@name'])
    print(a['tasks']['task'][0]['@name'])

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


def add_recipe():
    f = IngredientFactory()
    s = FoodSupervisor(db_location)
    i = [f.get_ingredient_ml('wodkaaaaa', 100)]
    m = MealFactory().get_meal_breakfast('Mil', 'Zrobic jedzenie xDDD', i)
    r = RecipeDay(m, m, m, m, m)
    s.add_recipe_day(r)

# add_recipe()
# x = get_recipes_ids()
# c = get_recipe(x[-2])
# print(c)

# m = MealLoaderFromFile('data/meal_test.txt')
# x = m.load_meals()
# s = FoodSupervisor('data/jedzonko.db')
# r = RecipeDay(x[0], x[1], x[2], x[3], x[4])
# s.add_recipe_day(r)
#
# print(get_recipe(2))

a = zFatFactory.get_fat(1)
print('xD')