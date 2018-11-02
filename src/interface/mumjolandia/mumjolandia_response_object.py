from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue


class MumjolandiaResponseObject:
    def __init__(self, status=MumjolandiaReturnValue.mumjolandia_none, arguments=[]):
        self.status = status
        self.arguments = arguments
