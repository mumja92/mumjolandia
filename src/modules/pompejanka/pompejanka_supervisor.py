import shutil
import textwrap
from datetime import datetime

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.utils.polish_utf_to_ascii import PolishUtfToAscii
from src.utils.shared_preferences import SharedPreferences
from src.utils.util_helpers import get_today_short


class PompejankaSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.start_date_string = 'pompejanka_start_date'
        self.start_date = SharedPreferences().get(self.start_date_string)
        if self.start_date is not None:
            self.start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):
        self.command_parsers['ls'] = self.__command_get
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['h'] = self.__command_help
        self.command_parsers['set'] = self.__command_set
        self.command_parsers['clear'] = self.__command_clear

    def __command_get(self, args):
        if self.start_date is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_get_ok,
                                             arguments=['Start date not set'])
        if self.__get_current_pompejanka_day() == 0:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_get_ok,
                                             arguments=['Done :D'])
        return_string = 'Current day: '
        return_string += str(self.__get_current_pompejanka_day()) + '\n'
        return_string += self.__print_pompejanka(self.__get_current_pompejanka_day())

        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_get_ok,
                                         arguments=[return_string])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.game_help,
                                         arguments=['set [x]\n'
                                                    'ls\n'
                                                    'clear\n'
                                                    '[h]elp'])

    def __command_set(self, args):
        if args is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.pompejanka_message,
                                             arguments=['Parameter not provided'])
        if int(args[0]) > 0:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.pompejanka_message,
                                             arguments=['Value has to be <= 0'])
        self.start_date = get_today_short(args[0])
        SharedPreferences().put(self.start_date_string, str(self.start_date))
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.pompejanka_message,
                                         arguments=['Set to: ' + str(get_today_short(args[0]))])

    def __command_clear(self, args):
        self.start_date = None
        SharedPreferences().clear_key(self.start_date_string)
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.pompejanka_message, arguments=['Clear ok'])

    def __get_current_pompejanka_day(self):
        if self.start_date is None:
            return -1
        day = int((get_today_short() - self.start_date).days) + 1
        if day > 54:
            return 0
        return day

    def __print_pompejanka(self, day):
        if day > 54:
            return "done :D"
        return_string = ('1. Znak krzyza\n'
                        '2. Podanie intencji\n'
                        '3. "Ten rozaniec odmawiam na Twoja czesc, Krolowo Rozanca Swietego\n'
                        '4. Wierze w Boga, Ojcze nasz, 3x Zdrowas Maryjo, Chwala Ojcu\n'
                        '5. 15 tajemnic rozanca\n'
                        '6. Modlitwa:\n'
                         )
        if day <= 27:
            return_string += PolishUtfToAscii.translate(self.__get_pompejanka_blagalna()) + '\n'
        else:
            return_string += PolishUtfToAscii.translate(self.__get_pompejanka_dziekczynna()) + '\n'
        return_string += ('7. Pod Twoja obrone\n'
                          '8. 3x "Krolowo rozanca swietego, modl sie za nami!"\n')
        return return_string

    def __get_pompejanka_blagalna(self):
        text = 'Pomnij o miłosierna Panno Różańcowa z Pompejów, jako nigdy jeszcze nie słyszano, aby ktokolwiek z czcicieli Twoich, z Różańcem Twoim, pomocy Twojej wzywający, miał być przez Ciebie opuszczony. Ach, nie gardź prośbą moją, o Matko Słowa Przedwiecznego, ale przez święty Twój różaniec i przez  upodobanie, jakie okazujesz dla Twojej świątyni w Pompejach wysłuchaj mnie dobrotliwie. Amen.'
        return textwrap.fill(text, shutil.get_terminal_size().columns)

    def __get_pompejanka_dziekczynna(self):
        text = 'Cóż Ci dać mogę, o Królowo pełna miłości? Moje całe życie poświęcam Tobie. Ile mi sił starczy, będę rozszerzać cześć Twoją, o Dziewico Różańca Świętego z Pompejów, bo gdy Twojej pomocy wezwałem, nawiedziła mnie łaska Boża. Wszędzie będę opowiadać o miłosierdziu, które mi wyświadczyłaś. O ile zdołam będę rozszerzać nabożeństwo do Różańca Świętego, wszystkim głosić będę, jak dobrotliwie obeszłaś się ze mną, aby i niegodni, tak jak i ja, grzesznicy, z zaufaniem do Ciebie się udawali. O, gdyby cały świat wiedział jak jesteś dobra, jaką masz litość nad cierpiącymi, wszystkie stworzenia uciekałyby się do Ciebie. Amen.'
        return textwrap.fill(text, shutil.get_terminal_size().columns)