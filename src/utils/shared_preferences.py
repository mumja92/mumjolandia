import logging

from src.utils.object_loader_pickle import ObjectLoaderPickle


class SharedPreferences:
    def __init__(self, filename='data/shared_preferences.pickle'):
        self.filename = filename
        self.object_loader = ObjectLoaderPickle(self.filename)

    def get(self, name):
        dictionary = self.object_loader.get()
        if not isinstance(dictionary, dict):
            logging.warning('Could not load file as dictionary: "' + self.filename + '"')
            return None
        try:
            return dictionary[name]
        except KeyError:
            return None

    def put(self, name, value):
        dictionary = self.object_loader.get()
        if dictionary is None:
            dictionary = {}
        dictionary[name] = value
        self.object_loader.save(dictionary)
