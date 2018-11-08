class Meal:
    def __init__(self, name, recipe, meal_type, ingredients=None):
        if ingredients is None:
            ingredients = []
        self.name = name
        self.type = meal_type
        self.recipe = recipe
        self.ingredients = ingredients

    def __str__(self):
        return_value = self.name + ' ' + str(self.type) + '\n'
        for i in self.ingredients:
            return_value += i.name + ' - ' + i.amount + ' [' + i.amount_type + ']' + '\n'
        return_value += 'Recipe: \n'
        return_value += self.recipe
        return return_value
