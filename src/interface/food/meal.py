from src.interface.mumjolandia.pod_template import PODTemplate


class Meal(PODTemplate):
    def __init__(self, name, recipe, meal_type, ingredients=None):
        if ingredients is None:
            ingredients = []
        self.name = name
        self.type = meal_type
        self.recipe = recipe
        self.ingredients = ingredients

    def get_recipe(self):
        return_value = self.name + ' [' + str(self.type.name) + ']\n'
        return_value += ' ' + self.recipe
        return return_value

    def __str__(self):
        return_value = self.name + ' [' + str(self.type.name) + ']\n'
        for i in self.ingredients:
            return_value += i.name + ' - ' + str(i.amount) + ' [' + i.amount_type.name + ']' + '\n'
        return_value += 'Recipe: \n'
        return_value += self.recipe
        return return_value
