from enum import Enum, unique


@unique
class MumjolandiaReturnValue(Enum):
    mumjolandia_none = 0
    mumjolandia_unrecognized_parameters = 11
    mumjolandia_unrecognized_command = 2
    mumjolandia_exit = 9
    # task
    task_added = 3
    task_name_not_given = 4
    task_help = 5
    task_null = 6
    task_get = 7
    task_incorrect_date_format = 8
    task_file_broken = 10
    task_delete_success = 12
    task_delete_incorrect_index = 1
    task_delete_incorrect_name = 13
    task_edit_ok = 14
    task_edit_wrong_index = 15
    #food
    food_get_wrong_index = 16
    food_get_ok = 17
    food_help = 18
    food_file_broken = 19
