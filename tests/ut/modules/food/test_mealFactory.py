from unittest import TestCase

from src.interface.food.food_sql_enums import MealType, AmountType
from src.modules.food.ingredient_factory import IngredientFactory
from src.modules.food.meal_factory import MealFactory


class TestMealFactory(TestCase):
    def test_get_meal(self):
        i = [IngredientFactory.get_ingredient('Maść', 10, AmountType.ml),
             IngredientFactory.get_ingredient('Inne', 1, AmountType.g)]
        m = MealFactory.get_meal('nazwa', 'przepis', MealType.breakfast, i)
        self.assertEqual(m.name, 'nazwa')
        self.assertEqual(m.recipe, 'przepis')
        self.assertEqual(len(m.ingredients), 2)
        self.assertEqual(m.ingredients[0], IngredientFactory.get_ingredient('Maść', 10, AmountType.ml))
        self.assertEqual(m.ingredients[1], IngredientFactory.get_ingredient('Inne', 1, AmountType.g))
