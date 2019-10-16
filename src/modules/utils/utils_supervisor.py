from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.utils.polish_utf_to_ascii import PolishUtfToAscii


class UtilsSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):

        self.command_parsers['help'] = self.__command_help
        self.command_parsers['p'] = self.__command_pompejanka
        self.command_parsers['pompejanka'] = self.__command_pompejanka

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_help,
                                         arguments=['[p]ompejanka\n'])

    def __command_pompejanka(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_get,
                                         arguments=['1. Znak krzyza\n'
                                                    '2. Podanie intencji\n'
                                                    '3. "Ten rozaniec odmawiam na Twoja czesc, Ktolowo Rozanca Swietego\n'
                                                    '4. Wierze w Boga, Ojcze nasz, 3x Zdrowas Maryjo, Chwala Ojcu\n'
                                                    '5. 15 tajemnic rozanca\n'
                                                    '6. Modlitwa a (pierwsze 27 dni) lub b (drugie 27 dni)\n'
                                                    '6a. \n' +
                                                    PolishUtfToAscii.translate(self.__get_pompejanka_blagalna()) + '\n'
                                                    '6b. \n' +
                                                    PolishUtfToAscii.translate(self.__get_pompejanka_dziekczynna()) + '\n'
                                                    '7. Pod Twoja obrone\n'
                                                    '8. "Krolowo rozanca swietego, modl sie za nami!"\n'
                                                    ])

    def __get_pompejanka_blagalna(self):
        return 'Pomnij o miłosierna Panno Różańcowa z Pompejów, jako nigdy jeszcze nie słyszano, aby ktokolwiek z czcicieli Twoich, z Różańcem Twoim, pomocy Twojej wzywający, miał być przez Ciebie opuszczony. Ach, nie gardź prośbą moją, o Matko Słowa Przedwiecznego, ale przez święty Twój różaniec i przez  upodobanie, jakie okazujesz dla Twojej świątyni w Pompejach wysłuchaj mnie dobrotliwie. Amen.'

    def __get_pompejanka_dziekczynna(self):
        return 'Cóż Ci dać mogę, o Królowo pełna miłości? Moje całe życie poświęcam Tobie. Ile mi sił starczy, będę rozszerzać cześć Twoją, o Dziewico Różańca Świętego z Pompejów, bo gdy Twojej pomocy wezwałem, nawiedziła mnie łaska Boża. Wszędzie będę opowiadać o miłosierdziu, które mi wyświadczyłaś. O ile zdołam będę rozszerzać nabożeństwo do Różańca Świętego, wszystkim głosić będę, jak dobrotliwie obeszłaś się ze mną, aby i niegodni, tak jak i ja, grzesznicy, z zaufaniem do Ciebie się udawali. O, gdyby cały świat wiedział jak jesteś dobra, jaką masz litość nad cierpiącymi, wszystkie stworzenia uciekałyby się do Ciebie. Amen.'
