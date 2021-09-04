from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.planner.plan import Plan


class MumjolandiaResultParser:
    def __init__(self):
        self.response_dict = {'default': self.__parse_default,
                              MumjolandiaReturnValue.planner_get_ok.name: self.__parse_planner_get_ok,
                              MumjolandiaReturnValue.task_find.name: self.__parse_task_find,
                              MumjolandiaReturnValue.task_get.name: self.__parse_task_ls,
                              }

    def parse(self, mumjolandia_response_object):
        try:
            return self.response_dict[mumjolandia_response_object.status.name](mumjolandia_response_object)
        except KeyError:
            return self.response_dict['default'](mumjolandia_response_object)

    def __parse_default(self, response_object):
        return str(response_object.status) + "\n" + str(response_object.arguments)

    def __parse_planner_get_ok(self, response_object):
        return_value = ""
        return_value += str(response_object.status) + "\n"
        if isinstance(response_object.arguments[0], Plan):  # if there is only one plan - arg[0] is plan object
            return_value += str(response_object.arguments[0])
        else:   # if there is more plans - arg[0] is list object with plans
            for plan in response_object.arguments[0]:
                return_value += str(plan)
        return return_value

    def __parse_task_find(self, response_object):
        return_value = str(response_object.status) + "\n"
        for index, task in zip(response_object.arguments[0], response_object.arguments[1]):
            return_value += str(index) + "\t" + str(task) + "\n"
        return return_value

    def __parse_task_ls(self, response_object):
        return_value = str(response_object.status) + "\n"
        for index, task in zip(response_object.arguments[0], response_object.arguments[1]):
            return_value += str(index) + "\t" + str(task) + "\n"
        return return_value
