from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.event.event_loader import EventLoader


class EventSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location):
        super().__init__()
        self.event_file_location = file_location
        self.event_loader = EventLoader(self.event_file_location)
        self.events = None
        self.__init()

    def __init(self):
        self.__add_command_parsers()
        self.events = self.event_loader.get()

    def __add_command_parsers(self):
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['help'] = self.__command_help

    def __command_get(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.event_get_ok, arguments=[self.events])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.event_help,
                                         arguments=['print'])
