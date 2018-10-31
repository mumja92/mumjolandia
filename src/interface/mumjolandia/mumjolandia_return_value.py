from enum import Enum, unique


@unique
class MumjolandiaReturnValue(Enum):
    none = 0
    ok = 1
    unrecognized_command = 2
    exit = 9
    # task
    task_added = 3
    task_name_not_given = 4
    task_help = 5
    task_null = 6
    task_print = 7
    task_incorrect_date_format = 8
    task_file_broken = 10
