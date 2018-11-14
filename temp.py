# db browser for sqlite
from src.interface.food.recipe_day import RecipeDay
from src.modules.food.food_database_helper import FoodDatabaseHelper
from src.modules.food.food_supervisor import FoodSupervisor
from src.modules.food.ingredient_factory import IngredientFactory
from src.modules.food.meal_factory import MealFactory
from src.modules.food.utils.meal_loader_from_file import MealLoaderFromFile

db_location = 'data/jedzonko2.db'


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
    print(x)


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
# get_recipe(x[-2])
#
# print(x)

# m = MealLoaderFromFile('data/meal_test.txt')
# x = m.load_meals()
# print(x)
xml_to_dict()