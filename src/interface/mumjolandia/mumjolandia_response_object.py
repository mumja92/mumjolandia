from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue


class MumjolandiaResponseObject:
    def __init__(self, status=MumjolandiaReturnValue.none, arguments=[]):
        self.status = status
        self.arguments = arguments
