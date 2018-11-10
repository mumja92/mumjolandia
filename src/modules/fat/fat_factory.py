from src.interface.fat.fat import Fat
from src.interface.mumjolandia.incorrect_variable_type_exception import IncorrectVariableTypeException
from src.interface.mumjolandia.incorrect_date_format_exception import IncorrectDateFormatException
import datetime


class FatFactory:
    @staticmethod
    def get_fat(value='unknown',
                 date_added=datetime.date.today()):
        try:
            if isinstance(date_added, str):
                date_added = datetime.datetime.strptime(date_added, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            raise IncorrectDateFormatException
        try:
            v = float(value)
        except ValueError:
            raise IncorrectVariableTypeException()
        return Fat(v, date_added)
