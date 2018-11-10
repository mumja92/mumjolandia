import logging
import pickle


class ObjectLoaderPickle:
    def __init__(self, file_name):
        self.file = file_name

    def get(self):
        objects = []
        try:
            with open(self.file, 'rb') as fi:
                objects = pickle.load(fi)
        except FileNotFoundError:
            logging.info(self.file + " - file doesn't exist")
            objects = []
        return objects

    def save(self, tasks):
        with open(self.file, 'wb') as fi:
            pickle.dump(tasks, fi)
