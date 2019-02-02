from src.interface.mumjolandia.pod_template import PODTemplate


class RecipeDay(PODTemplate):
    def __init__(self, breakfast, second_breakfast, dinner, tea, supper):
        self.breakfast = breakfast
        self.second_breakfast = second_breakfast
        self.dinner = dinner
        self.tea = tea
        self.supper = supper

    def __str__(self):
        return_value = self.breakfast.get_recipe() + '\n\n'
        return_value += self.second_breakfast.get_recipe() + '\n\n'
        return_value += self.dinner.get_recipe() + '\n\n'
        return_value += self.tea.get_recipe() + '\n\n'
        return_value += self.supper.get_recipe() + '\n'
        return return_value

    def translate(self, x):
        return self.__str__().translate(x)
