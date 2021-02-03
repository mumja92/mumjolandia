from src.interface.food.food_file_broken_exception import FoodFileBrokenException
from src.interface.food.food_sql_enums import AmountType
from src.interface.food.ingredient import Ingredient
from src.interface.food.recipe_day import RecipeDay
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.food.food_database_helper import FoodDatabaseHelper
from src.modules.food.meal_factory import MealFactory
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor


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
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['ingredients'] = self.__command_ingredient
        self.command_parsers['i'] = self.__command_ingredient
        self.command_parsers['lists'] = self.__command_list
        self.command_parsers['l'] = self.__command_list
        self.command_parsers['ls'] = self.__command_list

    def __command_list(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_list_ok,
                                         arguments=[self.__get_database_indexes()])

    def __command_get(self, args):
        try:
            index = self.__get_database_indexes()[int(args[0])]
            recipe = self.get_recipe_day(index)
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_ok, arguments=[recipe])
        except (IndexError, ValueError):
            try:
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_wrong_index,
                                                 arguments=[args[0]])
            except IndexError:  # if args[0] is empty (parameter not given) it will throw IndexError again
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_wrong_index,
                                                 arguments=[''])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_help,
                                         arguments=[
                                             'get [id]\n'
                                             '[i]ngredients [id]\n'
                                             '[l]ist\n'
                                             ''])

    def __command_ingredient(self, args):
        try:
            recipe = self.get_recipe_day(self.__get_database_indexes()[int(args[0])])
        except (IndexError, ValueError):
            try:
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_wrong_index,
                                                 arguments=[args[0]])
            except IndexError:  # if args[0] is empty (parameter not given) it will throw IndexError again
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_get_wrong_index,
                                                 arguments=[''])
        ingredients_breakfast = []
        ingredients_second_breakfast = []
        ingredients_dinner = []
        ingredients_tea = []
        ingredients_supper = []
        for i in recipe.breakfast.ingredients:
            ingredients_breakfast.append(str(i.name) + ' - ' + str(i.amount) + ' ' + str(i.amount_type.name))
        for i in recipe.second_breakfast.ingredients:
            ingredients_second_breakfast.append(str(i.name) + ' - ' + str(i.amount) + ' ' + str(i.amount_type.name))
        for i in recipe.dinner.ingredients:
            ingredients_dinner.append(str(i.name) + ' - ' + str(i.amount) + ' ' + str(i.amount_type.name))
        for i in recipe.tea.ingredients:
            ingredients_tea.append(str(i.name) + ' - ' + str(i.amount) + ' ' + str(i.amount_type.name))
        for i in recipe.supper.ingredients:
            ingredients_supper.append(str(i.name) + ' - ' + str(i.amount) + ' ' + str(i.amount_type.name))
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.food_ingredient_ok,
                                         arguments=[(recipe.breakfast.name, ingredients_breakfast),
                                                    (recipe.second_breakfast.name, ingredients_second_breakfast),
                                                    (recipe.dinner.name, ingredients_dinner),
                                                    (recipe.supper.name, ingredients_tea),
                                                    (recipe.tea.name, ingredients_supper)])

    def __get_database_indexes(self):
        return_value = []
        for x in self.db_helper.get_recipes_ids():
            return_value.append(x[0])
        return return_value
