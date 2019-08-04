from enum import Enum

from src.interface.command.command import Command


class WordType(Enum):
    start = 1   # 'word
    none = 2    # word wo'rd
    quoted = 3  # 'word'
    end = 4     # word'


class CommandFactory:

    @staticmethod
    def get_command(value):
        if value is None:
            return None
        if isinstance(value, list):
            return CommandFactory.__parse_list(value)
        else:
            return CommandFactory.__parse_string(value)

    @staticmethod
    def __parse_list(passed_list):
        return_value = []
        for s in passed_list:
            return_value.append(CommandFactory.__parse_string(s))
        return return_value

    @staticmethod
    def __parse_string(string):
        if len(string) == 0 or string.isspace():
            return Command([''])
        else:
            s = string.split()
            start_recognized_flag = 0
            temp = []
            arguments = []
            for w in s:
                if start_recognized_flag == 0:
                    if CommandFactory.__get_word_type(w) == WordType.start:
                        start_recognized_flag = 1
                        temp += w
                    elif CommandFactory.__get_word_type(w) == WordType.quoted:
                        arguments.append(w[1:-1])
                    else:
                        arguments.append(w)

                else:
                    if CommandFactory.__get_word_type(w) == WordType.end:
                        start_recognized_flag = 0
                        temp += ' ' + w[:-1]
                        arguments.append(''.join(temp[1:]))
                        temp.clear()
                    elif CommandFactory.__get_word_type(w) == WordType.quoted:
                        temp += ' ' + w[1:-1]
                    else:
                        temp += ' ' + w
            if len(temp) != 0:
                arguments.extend(temp)
            return Command(arguments)

    @staticmethod
    def __get_word_type(word):
        if len(word) < 2:
            return WordType.none
        elif word.startswith("'") and word.endswith("'"):
            return WordType.quoted
        elif word.startswith("'"):
            return WordType.start
        elif word.endswith("'"):
            return WordType.end
        else:
            return WordType.none

