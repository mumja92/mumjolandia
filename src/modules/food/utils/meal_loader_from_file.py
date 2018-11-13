from src.interface.food.food_sql_enums import MealType
from src.modules.food.ingredient_factory import IngredientFactory
from src.modules.food.meal_factory import MealFactory

# example file:

# meal name
# description
# [meal_type]
# ingredient1 [amount] [amount_type]
# <>
# supper meal
# description of the second meal
# 5
# bread 1 1
# tea 1 2
# <>


class State:
    name = 0
    description = 1
    type = 2
    ingredient = 3


class MealLoaderFromFile:
    def __init__(self, filename):
        self.filename = filename

    def load_meals(self):
        with open(self.filename, 'r') as f:
            m_name = ''
            m_desc = ''
            m_type = 0
            ingredients = []
            meals = []
            state = State.name
            for line in f:
                if state == State.name:
                    ingredients.clear()
                    m_name = ' '.join(line.split())
                    state = State.description
                    continue
                if state == State.description:
                    m_desc = ' '.join(line.split())
                    state = State.type
                    continue
                if state == State.type:
                    m_type = int(line)
                    state = State.ingredient
                    continue
                if state == State.ingredient:
                    s = ''.join(line.split())
                    if s == '<>':
                        state = State.name
                        meals.append(MealFactory.get_meal(m_name, m_desc, MealType(m_type), ingredients))
                        continue
                    ingredients.append(self.__line_to_ingredient(line))
                    continue

        return meals

    def __line_to_ingredient(self, line):
        l = line.split()
        n = ' '.join(l[0:-2])
        i = IngredientFactory.get_ingredient(n, l[-2], l[-1])
        return i

if __name__ == '__main__':
    m = MealLoaderFromFile('xD')
