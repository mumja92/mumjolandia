from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.password.password_factory import PasswordFactory
from src.utils.object_loader_pickle import ObjectLoaderPickle
from src.utils.pydes_wrapper import PydesWrapper
from src.utils.shared_preferences import SharedPreferences


class PasswordSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location='data/passwords.pickle'):
        super().__init__()
        self.file_location = file_location
        self.passwords_encrypted = None
        self.password_loader = ObjectLoaderPickle(self.file_location)
        self.password_validation_string_pickle_name = 'password_validation_string'
        self.password_validation_string = SharedPreferences().get(self.password_validation_string_pickle_name)
        self.password_validation_magic_word = 'R U S Z A N I E'
        self.main_password = None
        self.__init()

    def __init(self):
        self.__add_command_parsers()
        self.passwords_encrypted = self.password_loader.get()
        if self.passwords_encrypted is None:
            self.passwords_encrypted = []

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['init'] = self.__command_init
        self.command_parsers['ls'] = self.__command_list
        self.command_parsers['rm'] = self.__command_rm
        self.command_parsers['set'] = self.__command_set

    def __command_add(self, args):
        if self.main_password is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_not_set)
        if len(args) < 3:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_incorrect_value)
        new_name = args[0]
        new_username = args[1]
        new_password = args[2]
        password = PasswordFactory().get_password(self.main_password, new_password, new_name, new_username)
        self.passwords_encrypted.append(password)
        self.password_loader.save(self.passwords_encrypted)
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_add_ok,
                                         arguments=[password.name])

    def __command_get(self, args):
        if self.main_password is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_not_set)
        if len(args) < 1:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_incorrect_value, arguments=[])
        password = None
        for p in self.passwords_encrypted:
            if p.name == args[0]:
                password = p
        if password is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_incorrect_value, arguments=[])
        else:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_get_ok,
                                             arguments=[password.name,
                                                        PydesWrapper().decrypt(self.main_password, password.username),
                                                        PydesWrapper().decrypt(self.main_password, password.password)])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_help,
                                         arguments=['add [name]\n'
                                                    'get [name]\n'
                                                    'help\n'
                                                    'init [password]\n'
                                                    'ls\n'
                                                    'rm [name]\n'
                                                    'set [password]\n'
                                                    ])

    def __command_init(self, args):
        if len(args) < 1:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_incorrect_value, arguments=[])

        validation_ok = self.__create_password_validation_string(args[0])
        if validation_ok:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_set_ok)
        else:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_incorrect_value)

    def __command_list(self, args):
        if self.main_password is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_not_set)
        return_value = []
        for p in self.passwords_encrypted:
            return_value.append(p.name)
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_list_ok, arguments=[return_value])

    def __command_rm(self, args):
        if self.main_password is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_not_set)
        password = None
        for p in self.passwords_encrypted:
            if p.name == args[0]:
                password = p
        if password is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_incorrect_value, arguments=[])
        self.passwords_encrypted.remove(password)
        self.password_loader.save(self.passwords_encrypted)
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_rm_ok, arguments=['ok'])

    def __command_set(self, args):
        if len(args) < 1:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_incorrect_value, arguments=[])
        else:
            if self.__check_password_validation_string(args[0]):
                self.main_password = args[0]
            else:
                self.main_password = None
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_set_incorrect,
                                                 arguments=[args[0]])
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.password_set_ok)

    def __create_password_validation_string(self, password):
        self.password_validation_string = PydesWrapper().encrypt(password, self.password_validation_magic_word)
        if self.password_validation_string is not None:
            SharedPreferences().put(self.password_validation_string_pickle_name, self.password_validation_string)
            return True
        return False

    def __check_password_validation_string(self, password):
        decrypted_magic_word = str(PydesWrapper().decrypt(password, self.password_validation_string))
        if self.password_validation_magic_word == decrypted_magic_word:
            return True
        return False

    def __is_command_init_done(self):
        if self.password_validation_string is not None:
            return True
        return False
