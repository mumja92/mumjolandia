from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.planner.plans_handler import PlansHandler
from src.utils.object_loader_pickle import ObjectLoaderPickle


class PlannerSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location='data/plans.pickle'):
        super().__init__()
        self.file_location = file_location
        self.plans_handler = PlansHandler(self.file_location)
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['ls'] = self.__command_get
        self.command_parsers['remove'] = self.__command_remove
        self.command_parsers['rm'] = self.__command_remove
        self.command_parsers['help'] = self.__command_help
        self.command_parsers['h'] = self.__command_help

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.planner_help,
                                         arguments=['[h]elp'])

    def __command_get(self, args):
        try:
            day = int(args[0])
        except ValueError:  # argument is not int
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.planner_get_fail,
                                             arguments=['nook'])
        except IndexError:  # argument doesn't exist
            day = None
        return_value = self.plans_handler.get(day)
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.planner_get_ok,
                                         arguments=[return_value])

    def __command_add(self, args):
        day = None
        hour = None
        duration = None
        name = None
        try:
            day = int(args[0])
            hour = str(args[1])
            duration = int(args[2])
            name = str(args[3])
        except (ValueError, IndexError):  # one of arguments doesn't exist, or int(x) failed
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.planner_add_fail,
                                             arguments=['Incorrect argument: day: ' + str(day) + ' hour: ' + str(hour) + ' duration: ' + str(duration) + ' name: ' + str(name)])
        return_value = self.plans_handler.add(day, hour, duration, name)
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.planner_add_ok,
                                         arguments=[return_value])

    def __command_remove(self, args):
        day = None
        hour = None
        try:
            day = int(args[0])
            hour = str(args[1])
        except (ValueError, IndexError):  # one of arguments doesn't exist, or int(x) failed
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.planner_remove_fail,
                                             arguments=['Incorrect argument: day: ' + str(day) + ' hour: ' + str(hour)])
        return_value = self.plans_handler.remove(day, hour)
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.planner_remove_ok,
                                         arguments=[return_value])
