from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.interface.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.modules.note.note_factory import NoteFactory
from src.utils.object_loader_pickle import ObjectLoaderPickle


class NoteSupervisor(MumjolandiaSupervisor):
    def __init__(self, file_location):
        super().__init__()
        self.file_location = file_location
        self.note_loader = ObjectLoaderPickle(self.file_location)
        self.notes = None
        self.__init()

    def get_notes(self):
        return self.notes

    def add_note(self, name):
        self.notes.append(NoteFactory.get_note(name))
        self.__save()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_add_ok, arguments=[name])

    def delete_note(self, note_id):
        try:
            tid = int(note_id)
            try:
                self.notes.pop(tid)
                self.__save()
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_delete_success,
                                                 arguments=[note_id, str(1)])
            except IndexError:  # wrong index
                return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_delete_incorrect_index,
                                                 arguments=[note_id])
        except ValueError:  # parameter type is not int
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_delete_incorrect_index,
                                             arguments=[note_id])

    def __init(self):
        self.__add_command_parsers()
        self.notes = self.note_loader.get()
        if self.notes is None:
            self.notes = []

    def __save(self):
        self.note_loader.save(self.notes)

    def __add_command_parsers(self):
        self.command_parsers['add'] = self.__command_add
        self.command_parsers['get'] = self.__command_get
        self.command_parsers['rm'] = self.__command_delete
        self.command_parsers['help'] = self.__command_help

    def __command_add(self, args):
        if len(args) < 1:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_add_nook)
        else:
            return self.add_note(' '.join(args[0:]))

    def __command_get(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_get_ok, arguments=self.notes)

    def __command_delete(self, args):
        try:
            return self.delete_note(args[0])
        except IndexError:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_delete_incorrect_index,
                                             arguments=['none'])

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.note_help,
                                         arguments=['ls\n'
                                                    'add [name]\n'
                                                    'rm [id]\n'])
