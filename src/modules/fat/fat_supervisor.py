import logging

from src.interface.mumjolandia.incorrect_date_format_exception import IncorrectDateFormatException
from src.interface.mumjolandia.incorrect_variable_type_exception import IncorrectVariableTypeException
from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.fat.fat_factory import FatFactory
from src.utils.object_loader_pickle import ObjectLoaderPickle


class FatSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location):
        super().__init__()
        self.file_location = file_location
        self.fat_loader = ObjectLoaderPickle(self.file_location)
        self.fats = None
        self.__init()

    def get_fats(self):
        return self.fats

    def add_fat(self, value):
        try:
            self.fats.append(FatFactory.get_fat(value))
        except IncorrectDateFormatException:
            logging.warning("Fat '" + value + "' not added - incorrect date format")
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_incorrect_date_format)
        except IncorrectVariableTypeException:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_add_must_be_float)
        logging.info("Added '" + value + "'")
        self.__save()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_added, arguments=[value])

    def delete_fat(self, fat_id):
        # parameter comes as string. If we can parse it to int then we remove by id. If not, then by name
        try:
            fid = int(fat_id)
            try:
                self.fats.pop(fid)
                self.__save()
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_delete_success,
                                                 arguments=[fat_id, str(1)])
            except IndexError:  # wrong index
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_delete_incorrect_index,
                                                 arguments=[fat_id])
        except ValueError:  # parameter type is not int
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_delete_incorrect_index,
                                             arguments=[fat_id])

    def __init(self):
        self.__add_command_parsers()
        self.fats = self.fat_loader.get()

    def __save(self):
        logging.debug("saving tasks to: '" + self.file_location + "'")
        self.fat_loader.save(self.fats)

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['delete'] = self.__command_delete

    def __command_add(self, args):
        if len(args) < 1:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_value_not_given)
        else:
            return self.add_fat(args[0])

    def __command_get(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_get_ok, arguments=self.fats)

    def __command_delete(self, args):
        try:
            return self.delete_fat(args[0])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.fat_delete_incorrect_index,
                                             arguments=['none'])
