import os
from pathlib import Path


class RootFSManager:
    def __init__(self):
        self.__current_directory = "."

    def cd(self, path=None):
        if path is None:
            self.__current_directory = "."
        elif os.path.isdir(Path.joinpath(Path(self.__get_cwd()), path)):
            self.__current_directory = Path.joinpath(Path(self.__get_cwd()), path)
        return self.__get_cwd()

    def pwd(self):
        return self.__get_cwd()

    def ls(self, path="."):
        try:
            command_args = str(path)
        except IndexError:
            command_args = "."
        try:
            dir_content = os.listdir(Path.joinpath(Path(self.__get_cwd()), path))
        except FileNotFoundError:
            dir_content = None

        if dir_content is None:
            return None
        else:
            return_value = []
            cwd_path = Path(self.__get_cwd())
            cwd_path = cwd_path.joinpath(command_args)
            for entity in dir_content:
                if cwd_path.joinpath(entity).is_dir():
                    return_value.append("&" + entity)
                else:
                    return_value.append("*" + entity)
        return '\n'.join(return_value)

    def __get_cwd(self):
        return os.path.normpath(Path.joinpath(Path(os.getcwd()), self.__current_directory).absolute())
