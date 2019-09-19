import logging

from src.utils.object_loader_pickle import ObjectLoaderPickle


class SharedPreferences:
    def __init__(self, filename='data/shared_preferences.pickle'):
        self.filename = filename
        self.object_loader = ObjectLoaderPickle(self.filename)

    def get(self, name):
        dictionary = self.__get_dict()
        if dictionary is None:
            return_value = None
        else:
            try:
                return_value = dictionary[name]
            except KeyError:
                return_value = None
        return return_value

    def put(self, name, value):
        dictionary = self.__get_dict()
        if dictionary is None:
            return_value = False
        else:
            dictionary[name] = value
            self.object_loader.save(dictionary)
            return_value = True
        return return_value

    def clear_key(self, key):
        return_value = None
        dictionary = self.__get_dict()
        if dictionary is not None:
            if dictionary.pop(key, None) is not None:
                return_value = True
            else:
                return_value = False
        if return_value:
            self.object_loader.save(dictionary)
        return return_value

    def clear_starting_pattern(self, starting_pattern):
        return_value = 0
        dictionary = self.__get_dict()
        if dictionary is not None:
            for k in list(dictionary):
                if k.startswith(starting_pattern):
                    del dictionary[k]
                    return_value += 1
        if return_value != 0:
            self.object_loader.save(dictionary)
        return return_value

    def __get_dict(self):
        dictionary = self.object_loader.get()
        if dictionary is None:
            dictionary = {}
        elif not isinstance(dictionary, dict):
            logging.error('Could not load file as dictionary: "' + self.filename + '"')
            dictionary = None
        return dictionary
