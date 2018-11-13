from src.interface.food.recipe_day import RecipeDay


class RecipeDayFactory:
    @staticmethod
    def get_recipe_day(breakfast=None, second_breakfast=None, dinner=None, tea=None, supper=None):
        return RecipeDay(breakfast, second_breakfast, dinner, tea, supper)
