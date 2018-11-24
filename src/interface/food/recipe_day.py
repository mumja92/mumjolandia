from src.interface.mumjolandia.pod_template import PODTemplate


class RecipeDay(PODTemplate):
    def __init__(self, breakfast, second_breakfast, dinner, tea, supper):
        self.breakfast = breakfast
        self.second_breakfast = second_breakfast
        self.dinner = dinner
        self.tea = tea
        self.supper = supper

    def __str__(self):
        return_value = 'Breakast: \n'
        return_value += str(self.breakfast) + '\n\n'
        return_value += 'Second breakast: \n'
        return_value += str(self.second_breakfast) + '\n\n'
        return_value += 'Dinner: \n'
        return_value += str(self.dinner) + '\n\n'
        return_value += 'Tea: \n'
        return_value += str(self.tea) + '\n\n'
        return_value += 'Supper: \n'
        return_value += str(self.supper)
        return return_value

    def translate(self, x):
        return self.__str__().translate(x)
