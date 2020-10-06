import logging
import pickle


class ObjectLoaderPickle:
    def __init__(self, file_name):
        self.file = file_name

    def get(self):
        try:
            with open(self.file, 'rb') as fi:
                data = pickle.load(fi)
        except FileNotFoundError:
            logging.debug(self.file + " - file doesn't exist")
            data = None
        return data

    def save(self, data):
        with open(self.file, 'wb') as fi:
            pickle.dump(data, fi)
