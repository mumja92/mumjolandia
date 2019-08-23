# db browser for sqlite

from src.interface.food.recipe_day import RecipeDay
from src.modules.connection.connection_supervisor import SocketServer
from src.modules.food.food_database_helper import FoodDatabaseHelper
from src.modules.food.food_supervisor import FoodSupervisor
from src.modules.food.ingredient_factory import IngredientFactory
from src.modules.food.meal_factory import MealFactory
from src.modules.game.game_loader import GameLoader

db_location = 'data/jedzonko.db'


def xml_to_dict():
    from src.external.xmltodict import xmltodict
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


# p = PeriodicTasksGenerator('data/periodic_tasks.xml')
# x = p.get_list_next_occurrence()
# for t in x:
#     print(t)

# gl = GameLoader('data/games.xml')
# xD = gl.get()
# print(xD)

s = SocketServer('localhost', 3333)
s.run_session()


class GameLoader:
    def __init__(self, filename):
        self.file = filename

    def get(self):
        games = GamesContainer()
        file = Path(self.file)
        if not file.is_file():
            return games
        with open(self.file, 'r') as my_file:
            data = my_file.read()
        d = xmltodict.parse(data)
        for game_type in GameType:
            if isinstance(d['games'][game_type.name], type(None)):              # node empty
                continue
            elif isinstance(d['games'][game_type.name]['game'], str):           # node has 1 element
                games.add(str(d['games'][game_type.name]['game']), game_type)
            elif isinstance(d['games'][game_type.name]['game'], list):          # node has many elements
                for g in d['games'][game_type.name]['game']:
                    games.add(GameFactory().get_game(name=g, game_type=game_type), game_type)
        return games

    def save(self):
        pass
