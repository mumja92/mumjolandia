import logging
import os
import shutil
import zipfile
import urllib.request
import ssl

from pathlib import Path

from src.utils.helpers import RandomUtils

try:
    from distutils.dir_util import copy_tree
    distutils_available = True
except ModuleNotFoundError:
    distutils_available = False
from urllib.error import HTTPError

from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.modules.mumjolandia.config_loader import ConfigLoader
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor
from src.utils.shared_preferences import SharedPreferences


class UtilsSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.__init()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):

        self.command_parsers['help'] = self.__command_help
        self.command_parsers['ip'] = self.__command_ip
        self.command_parsers['location'] = self.__command_location
        self.command_parsers['l'] = self.__command_location
        self.command_parsers['preferences'] = self.__command_preferences
        self.command_parsers['p'] = self.__command_preferences
        self.command_parsers['update'] = self.__command_update
        self.command_parsers['u'] = self.__command_update

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_help,
                                         arguments=[
                                             'ip\n'
                                             '[l]ocation\n'
                                             '[p]references\n'
                                             '[u]pdate {branch}\n'
                                         ])

    def __command_ip(self, args):
        ip_address = RandomUtils.get_ip()
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_get,
                                         arguments=[str(ip_address)])

    def __command_location(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_get,
                                         arguments=[ConfigLoader.get_mumjolandia_location()])

    def __command_preferences(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_shared_preferences_get,
                                         arguments=[SharedPreferences().get_all()])

    def __command_update(self, args):
        if not distutils_available:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_update_fail,
                                             arguments=['Distutils not available. Please run \'sudo apt install python3-distutils\''])
        branch = "master"
        if len(args):
            branch = args[0]
        mumjolandia_path = "https://github.com/mumja92/mumjolandia/archive/" + branch + ".zip"
        update_dir = ConfigLoader.get_mumjolandia_location() + "update_dir/"
        file_name = "mumjolandia.zip"
        if os.path.exists(update_dir):
            shutil.rmtree(update_dir)
        Path(update_dir).mkdir(exist_ok=True)
        try:
            ssl._create_default_https_context = ssl._create_unverified_context  # SSL: CERTIFICATE_VERIFY_FAILED on qpython
            urllib.request.urlretrieve(mumjolandia_path, update_dir + file_name)
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            shutil.rmtree(update_dir)
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_update_fail,
                                             arguments=[str(e)])

        with zipfile.ZipFile(update_dir + file_name, 'r') as archive:
            archive.extract(member='mumjolandia-' + branch + '/main.py', path=update_dir)
            for file in archive.namelist():
                if file.startswith('mumjolandia-' + branch + '/src/'):
                    archive.extract(file, update_dir)

        shutil.rmtree(ConfigLoader.get_mumjolandia_location() + 'src')
        try:
            os.remove(ConfigLoader.get_mumjolandia_location() + 'main.py')
        except OSError:
            pass
        copy_tree(update_dir + 'mumjolandia-' + branch, ConfigLoader.get_mumjolandia_location())
        shutil.rmtree(update_dir)

        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_update_ok,
                                         arguments=[branch])
