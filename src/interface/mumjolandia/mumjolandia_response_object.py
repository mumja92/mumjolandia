from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.pod_template import PODTemplate


class MumjolandiaResponseObject(PODTemplate):
    def __init__(self, status=MumjolandiaReturnValue.mumjolandia_none, arguments=None):
        self.status = status
        self.arguments = arguments
        if self.arguments is None:
            self.arguments = []
