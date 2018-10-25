from enum import Enum

from src.interface.command.command import Command


class WordType(Enum):  # if word starts with ' then WordType = 1
    start = 1   # 'word
    none = 2    # word wo'rd
    quoted = 3  # 'word'
    end = 4     # word'


class CommandFactory:

    @staticmethod
    def get_command(string):
        if len(string) == 0 or string.isspace():
            return Command([''])
        else:
            s = string.split()
            start_recognized_flag = 0
            temp = []
            arguments = []
            for w in s:
                if start_recognized_flag == 0:
                    if CommandFactory.get_word_type(w) == WordType.start:
                        start_recognized_flag = 1
                        temp += w
                    elif CommandFactory.get_word_type(w) == WordType.quoted:
                        arguments.append(w[1:-1])
                    else:
                        arguments.append(w)

                else:
                    if CommandFactory.get_word_type(w) == WordType.end:
                        start_recognized_flag = 0
                        temp += ' ' + w[:-1]
                        arguments.append(''.join(temp[1:]))
                        temp.clear()
                    elif CommandFactory.get_word_type(w) == WordType.quoted:
                        temp += ' ' + w[1:-1]
                    else:
                        temp += ' ' + w
            if len(temp) != 0:
                arguments.extend(temp)
            return Command(arguments)

    @staticmethod
    def get_word_type(word):
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

