from unittest import TestCase

from src.interface.food.food_sql_enums import AmountType
from src.modules.food.ingredient_factory import IngredientFactory


class TestIngredientFactory(TestCase):
    def test_get_ingredient_empty(self):
        x = IngredientFactory.get_ingredient()
        self.assertEqual(x.name, 'error')
        self.assertEqual(x.amount, 0)
        self.assertEqual(x.amount_type, AmountType.error)

    def test_get_ingredient_filled(self):
        x = IngredientFactory.get_ingredient('Name', 1, AmountType.ml)
        self.assertEqual(x.name, 'Name')
        self.assertEqual(x.amount, 1)
        self.assertEqual(x.amount_type, AmountType.ml)

    def test_get_ingredient_filled_with_value(self):
        x = IngredientFactory.get_ingredient('Name', 1, 4)
        self.assertEqual(x.name, 'Name')
        self.assertEqual(x.amount, 1)
        self.assertEqual(x.amount_type, AmountType.ml)

    def test_get_ingredient_filled_with_bad_input(self):
        x = IngredientFactory.get_ingredient(1, 'string', 'ml')
        self.assertEqual(x.name, 'error')
        self.assertEqual(x.amount, -1)
        self.assertEqual(x.amount_type, AmountType.error)
