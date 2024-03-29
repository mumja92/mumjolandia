from src.interface.mumjolandia.mumjolandia_response_object import MumjolandiaResponseObject
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.utils.rootfs_manager import RootFSManager
from src.modules.mumjolandia.mumjolandia_supervisor import MumjolandiaSupervisor


class RootFSSupervisor(MumjolandiaSupervisor):
    def __init__(self):
        super().__init__()
        self.__init()
        self.rootfs_manager = RootFSManager()

    def __init(self):
        self.__add_command_parsers()

    def __add_command_parsers(self):

        self.command_parsers['help'] = self.__command_help
        self.command_parsers['pwd'] = self.__command_pwd
        self.command_parsers['ls'] = self.__command_ls
        self.command_parsers['cd'] = self.__command_cd

    def __command_help(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.utils_help,
                                         arguments=[
                                             'cd [path]\n'
                                             'ls [path]\n'
                                             'pwd\n'
                                         ])

    def __command_pwd(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.rootfs_pwd_ok,
                                         arguments=[self.rootfs_manager.pwd()])

    def __command_ls(self, args):
        response = self.rootfs_manager.ls(" ".join(args))
        if response is None:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.rootfs_no_ok,
                                         arguments=["Incorrect path"])
        else:
            return MumjolandiaResponseObject(status=MumjolandiaReturnValue.rootfs_ls_ok,
                                             arguments=[response])

    def __command_cd(self, args):
        return MumjolandiaResponseObject(status=MumjolandiaReturnValue.rootfs_pwd_ok,
                                         arguments=[self.rootfs_manager.cd(" ".join(args))])
