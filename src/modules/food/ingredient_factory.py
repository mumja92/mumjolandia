from src.interface.food.food_sql_enums import AmountType
from src.interface.food.ingredient import Ingredient


class IngredientFactory:
    @staticmethod
    def get_ingredient(name=None, amount=None, amount_type=None):
        a_type = amount_type
        if a_type is None:
            a_type = AmountType['error']
        elif not isinstance(a_type, AmountType):
            try:
                a_type = AmountType(int(amount_type))
            except ValueError:
                a_type = AmountType['error']
        am = 0
        if amount is not None:
            try:
                am = int(amount)
            except ValueError:
                am = -1
        na = 'error'
        if name is not None:
            try:
                if len(name) > 0 and isinstance(name, str):
                    na = name
            except TypeError:
                pass
        return Ingredient(na, am, a_type)
