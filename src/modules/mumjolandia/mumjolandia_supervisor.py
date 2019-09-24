import logging

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue


class MumjolandiaSupervisor:
    def __init__(self):
        self.command_parsers = {}
        self.__init()

    def execute(self, command):
        try:
            logging.info(self.__class__.__name__ + ' - parsing command: ' + str(command.arguments))
            return self.command_parsers[command.arguments[0]](command.arguments[1:])
        except KeyError:        # command parser doesn't exist
            logging.info('Unrecognized command: ' + str(command.arguments))
            return self.command_parsers['unrecognized_command'](command.arguments)
        except IndexError:
            return self.command_parsers['null'](command.arguments)
        except AttributeError:  # command == None
            return self.command_parsers['null']('')

    def __init(self):
        self.command_parsers['null'] = self.__command_null
        self.command_parsers['unrecognized_command'] = self.__unrecognized_command

    def __unrecognized_command(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.mumjolandia_unrecognized_parameters,
                                         arguments=args)

    def __command_null(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.mumjolandia_unrecognized_parameters,
                                         arguments=args)
