from unittest import TestCase

from src.interface.food.food_sql_enums import AmountType, MealType
from src.modules.food.ingredient_factory import IngredientFactory
from src.modules.food.meal_factory import MealFactory
from src.modules.food.recipe_day_factory import RecipeDayFactory


class TestRecipeDayFactory(TestCase):
    def test_get_recipe_day(self):
        i = [IngredientFactory.get_ingredient('Maść', 10, AmountType.ml)]
        m = MealFactory.get_meal('nazwa', 'przepis', MealType.breakfast, [i])
        m2 = MealFactory.get_meal('nazwa', 'przepis', MealType.second_breakfast, [i])
        m3 = MealFactory.get_meal('nazwaa', 'przepis', MealType.dinner, [i])
        m4 = MealFactory.get_meal('nazwaaa', 'przepis', MealType.tea, [i])
        m5 = MealFactory.get_meal('nazwaaaa', 'przepis', MealType.supper, [i])
        r = RecipeDayFactory.get_recipe_day(m, m2, m3, m4, m5)
        self.assertEqual(r.breakfast, m)
        self.assertEqual(r.second_breakfast, m2)
        self.assertEqual(r.dinner, m3)
        self.assertEqual(r.tea, m4)
        self.assertEqual(r.supper, m5)
