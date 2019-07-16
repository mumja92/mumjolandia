import logging
import os
import shutil
import sys
import tarfile
from os.path import realpath


class MumjolandiaUpdater:
    def __init__(self):
        pass

    @staticmethod
    def pack_source(filename='mumjolandia.tar.gz'):
        if os.path.isfile(filename):
            logging.info('Deleting old tar file')
            os.remove(filename)
        with tarfile.open(filename, "w:gz") as tar_handle:
            for root, dirs, files in os.walk(MumjolandiaUpdater.get_mumjolandia_location() + '/src'):
                for file in files:
                    if '.pyc' in file:
                        continue
                    file_path = os.path.join(root, file)
                    tar_handle.add(file_path, arcname=file_path.replace(MumjolandiaUpdater.get_mumjolandia_location(), ''))
        return realpath(filename)

    @staticmethod
    def install_source(file_location):
        try:
            with tarfile.open(file_location, "r:gz") as tar_handle:
                shutil.rmtree(MumjolandiaUpdater.get_mumjolandia_location() + '/src')
                tar_handle.extractall(MumjolandiaUpdater.get_mumjolandia_location())
            os.remove(file_location)
        except tarfile.ReadError as e:
            print("file broken")

    @staticmethod
    def get_mumjolandia_location():
        # return os.path.dirname(sys.modules['__main__'].__file__)
        return os.path.abspath(os.path.dirname(sys.argv[0]))
