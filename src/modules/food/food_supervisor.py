from src.interface.food.food_file_broken_exception import FoodFileBrokenException
from src.interface.food.food_sql_enums import AmountType
from src.interface.food.ingredient import Ingredient
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
        self.is_db_ok = self.db_helper.is_database_ok()
        self.__init()

    def execute(self, command):
        try:
            return super(FoodSupervisor, self).execute(command)
        except FoodFileBrokenException:
            return MumjolandiaResponseObject(MumjolandiaReturnValue.food_file_broken, [self.db_location])

    def get_recipe_day(self, recipe_id):
        if not self.is_db_ok:
            raise FoodFileBrokenException
        meal_ids = self.db_helper.get_recipes_day(recipe_id)
        return_value = RecipeDay(self.__get_meal(meal_ids[0][1]),
                                 self.__get_meal(meal_ids[0][2]),
                                 self.__get_meal(meal_ids[0][3]),
                                 self.__get_meal(meal_ids[0][4]),
                                 self.__get_meal(meal_ids[0][5]))
        return return_value

    def add_recipe_day(self, recipe):
        if not self.is_db_ok:
            raise FoodFileBrokenException
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
            ingredients.append(Ingredient(t[1].rstrip(), str(t[3]), AmountType[t[2].rstrip()]))
        m = MealFactory().get_meal(name, recipe, meal_type, ingredients)
        return m

    def __insert_meal(self, meal):
        meal_id = self.db_helper.get_meal_id_if_exists(meal.name, meal.recipe, meal.type.value)
        if meal_id is None:
            meal_id = self.db_helper.get_new_meal_id(meal.type.value, meal.name, meal.recipe)
        ingredient_list = []
        for i in meal.ingredients:
            ingredient_list.append([self.db_helper.get_ingredient_id(i.name), i.amount, i.amount_type])
        for l in ingredient_list:
            self.db_helper.insert_meal_ingredient(meal_id, l[0], l[2].value, l[1])
        return meal_id

    def __add_command_parsers(self):
        self.command_parsers['print'] = self.__command_print
        self.command_parsers['help'] = self.__command_help

    def __command_print(self, args):
        try:
            recipe = self.get_recipe_day(int(args[0]))
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_ok, arguments=[recipe])
        except (IndexError, ValueError):
            try:
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_wrong_index,
                                                 arguments=[args[0]])
            except IndexError:  # if args[0] is empty (parameter not given) it will throw IndexError again
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_wrong_index,
                                                 arguments=[''])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_help, arguments=['get [id]'])
