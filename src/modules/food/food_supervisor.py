from src.interface.food.ingredient import Ingredient
from src.interface.food.meal import Meal
from src.interface.food.recipe_day import RecipeDay
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.food.food_database_helper import FoodDatabaseHelper
from src.modules.food.meal_factory import MealFactory


class FoodSupervisor(MumjolandiaSupervisor):
    def __init__(self, db_location):
        super().__init__()
        self.db_location = db_location
        self.db_helper = FoodDatabaseHelper(self.db_location)
        self.__init()

    def get_recipe_day(self, recipe_id):
        meal_ids = self.db_helper.get_recipes_day(recipe_id)
        return_value = RecipeDay(self.__get_meal(meal_ids[0][1]),
                                 self.__get_meal(meal_ids[0][2]),
                                 self.__get_meal(meal_ids[0][3]),
                                 self.__get_meal(meal_ids[0][4]),
                                 self.__get_meal(meal_ids[0][5]))
        return return_value

    def add_recipe_day(self, recipe):
        ids = [self.__insert_meal(recipe.breakfast), self.__insert_meal(recipe.second_breakfast),
               self.__insert_meal(recipe.dinner), self.__insert_meal(recipe.tea), self.__insert_meal(recipe.supper)]
        self.db_helper.insert_recipe_day(ids[0], ids[1], ids[2], ids[3], ids[4])

    def __init(self):
        self.__add_command_parsers()

    def __get_meal(self, id_meal):
        dish = self.db_helper.select_meal_ingredients(id_meal)
        name = dish[0][0]
        ingredients = []
        recipe = self.db_helper.get_meal_recipe(id_meal)
        meal_type = self.db_helper.get_meal_type(id_meal)
        for t in dish:
            ingredients.append(Ingredient(t[1].rstrip(), str(t[3]), t[2].rstrip()))
        m = MealFactory().get_meal(name, recipe, meal_type, ingredients)
        return m

    def __insert_meal(self, meal):
        meal_id = self.db_helper.get_new_meal_id(meal)
        ingredient_list = []
        for i in meal.ingredients:
            ingredient_list.append([self.db_helper.get_ingredient_id(i.name), i.amount, i.amount_type])
        for l in ingredient_list:
            self.db_helper.insert_meal_ingredient(meal_id, l[0], l[2], l[1])
        return meal_id

    def __add_command_parsers(self):
        self.command_parsers['print'] = self.__command_print
        self.command_parsers['help'] = self.__command_help

    def __command_print(self, args):
        try:
            recipe = self.get_recipe_day(args[0])
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_ok, arguments=[recipe])
        except IndexError:
            try:
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_wrong_index,
                                                 arguments=[args[0]])
            except IndexError:  # if args[0] is empty (parameter not given) it will throw IndexError again
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_wrong_index,
                                                 arguments=[''])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_help, arguments=['get [id]'])
