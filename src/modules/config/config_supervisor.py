from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.config.config_parser import ConfigParser
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor


class ConfigSupervisor(MumjolandiaSupervisor):
    def __init__(self, config_path="config.xml"):
        super().__init__()
        self.config_file = config_path
        self.config_parser = ConfigParser(self.config_file)
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):

        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['set'] = self.__command_set

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_help,
                                         arguments=[
                                             'get [name]\n'
                                             'set [name] [value]\n'
                                         ])

    def __command_get(self, args):
        # argument not provided
        if not len(args):
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.config_get_fail,
                                             arguments=["Parameter needed"])

        return_value = self.config_parser.get(args[0])

        if return_value is not None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.config_get_ok,
                                             arguments=[return_value])
        else:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.config_get_fail,
                                             arguments=["Value \"" + args[0] + "\" not found"])

    def __command_set(self, args):
        if len(args) < 2:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.config_set_nook,
                                             arguments=["2 parameters needed"])

        if self.config_parser.set(args[0], args[1]):
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.config_set_ok,
                                             arguments=[self.config_parser.get(args[0])])
        else:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.config_set_nook,
                                             arguments=["Parameter \"" + args[0] + "\" not found"])
