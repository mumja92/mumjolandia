from src.interface.food.food_sql_enums import MealType
from src.modules.food.ingredient_factory import IngredientFactory
from src.modules.food.meal_factory import MealFactory

# example file:

# meal name
# description
# ingredient1 [amount] [amount_type_name]
# <>
# Kanapki z twarogiem
# -
# Chleb zytni 3 slice
# Ser twarogowy chudy 150 g
# Warzywka 1 a_little
# <>


class State:
    name = 0
    description = 1
    ingredient = 3


class MealLoaderFromFile:
    def __init__(self, filename):
        self.filename = filename

    # meal_type 1-5
    # if passed_meal_type is None load only 5 meals to be saved as complete 5-meal recipe
    def load_meals(self, passed_meal_type=None):
        with open(self.filename, 'r') as f:
            m_name = ''
            m_desc = ''
            m_type = 0
            ingredients = []
            meals = []
            state = State.name
            for line in f:
                if state == State.name:
                    ingredients = []
                    m_name = ' '.join(line.split())
                    state = State.description
                    continue
                if state == State.description:
                    m_desc = ' '.join(line.split())
                    state = State.ingredient
                    continue
                if state == State.ingredient:
                    s = ''.join(line.split())
                    if s == '<>':
                        state = State.name
                        if passed_meal_type is None:
                            m_type = self.__inc_meal_type(m_type)
                        else:
                            m_type = int(passed_meal_type)
                        meals.append(MealFactory.get_meal(m_name, m_desc, MealType(m_type), ingredients))
                        continue
                    ingredients.append(self.__line_to_ingredient(line))
                    continue

        return meals

    def __line_to_ingredient(self, line):
        l = line.split()
        n = ' '.join(l[0:-2])
        i = IngredientFactory.get_ingredient(n, l[-2], self.__line_to_type(l[-1]))
        return i

    def __line_to_type(self, line):
        amount_type = ''.join(line.split())
        if amount_type == 'g':
            return 1
        elif amount_type == 'number':
            return 2
        elif amount_type == 'a_little':
            return 3
        elif amount_type == 'ml':
            return 4
        elif amount_type == 'handful':
            return 5
        elif amount_type == 'slice':
            return 6
        elif amount_type == 'spoon':
            return 7
        else:
            print('ERROR ERROR ERROR')
            print('ERROR ERROR ERROR')
            print('ERROR ERROR ERROR')
            print('Dla: "' + str(line) + '"')
            return 0

    def __inc_meal_type(self, n):
        return_value = n + 1
        if return_value > 5:
            return_value = 1
        return return_value
