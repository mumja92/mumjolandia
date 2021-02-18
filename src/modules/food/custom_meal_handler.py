from src.utils.shared_preferences import SharedPreferences


class CustomMealHandler:
    def __init__(self):
        self.meal = []
        self.meal_string = 'custom_meal_handler_'
        self.__load_recipe()

    def set(self, recipe_index, which_meal_index):
        if not isinstance(recipe_index, int):
            return False
        if not isinstance(which_meal_index, int):
            return False
        if 0 > which_meal_index > 4:
            return False
        if recipe_index < 0:
            self.meal[which_meal_index] = None
        else:
            self.meal[which_meal_index] = recipe_index
        self.__save_recipe()
        return True

    def get(self):
        return self.meal

    def __load_recipe(self):
        for i in range(0, 5):
            saved_value = SharedPreferences().get(self.meal_string + str(i))
            if saved_value is None:
                self.meal.append(None)
            else:
                self.meal.append(int(saved_value))

    def __save_recipe(self):
        for i in range(0, 4):
            if self.meal[i] is None:
                SharedPreferences().clear_key(self.meal_string + str(i))
            else:
                SharedPreferences().put(self.meal_string + str(i), str(self.meal[i]))
