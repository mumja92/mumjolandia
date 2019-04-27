from src.interface.note.note import Note


class NoteFactory:
    @staticmethod
    def get_note(text='invalid'):
        return Note(str(text))
