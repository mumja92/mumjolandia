import logging
from src.utils.helpers import RandomUtils


class Notificator:
    def notify(self, title, text, function=None):
        platform = RandomUtils.get_platform()
        if platform == 'android':
            self.__notify_android(title, text, function)
            return True
        elif platform == 'linux':
            self.__notify_cli(title, text)
            return True
        elif platform == 'windows':
            self.__notify_cli(title, text)
            return True
        else:
            logging.warning('Unrecognized platform: ' + platform)
            return False

    def __notify_android(self, title, text, function=None):
        import androidhelper
        droid = androidhelper.Android()
        droid.notify(title, text, function)

    def __notify_cli(self, title, text):
        print(str(title).upper())
        print(text)
