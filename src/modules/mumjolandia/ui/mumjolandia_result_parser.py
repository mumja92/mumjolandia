from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue


class MumjolandiaResultParser:
    def __init__(self):
        self.response_dict = {'default': self.__parse_default,
                              MumjolandiaReturnValue.task_get.name: self.__parse_task_ls,
                              }

    def parse(self, mumjolandia_response_object):
        try:
            return self.response_dict[mumjolandia_response_object.status.name](mumjolandia_response_object)
        except KeyError:
            return self.response_dict['default'](mumjolandia_response_object)

    def __parse_default(self, response_object):
        return str(response_object.status) + "\n" + str(response_object.arguments)

    def __parse_task_ls(self, response_object):
        return_value = str(response_object.status) + "\n"
        for index, task in zip(response_object.arguments[0], response_object.arguments[1]):
            return_value += str(index) + "\t" + str(task) + "\n"
        return return_value
