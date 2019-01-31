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
    task_get_wrong_data = 33
    task_incorrect_date_format = 8
    task_file_broken = 10
    task_delete_success = 12
    task_delete_incorrect_index = 1
    task_delete_incorrect_name = 13
    task_edit_ok = 14
    task_edit_wrong_index = 15
    task_set_incorrect_parameter = 34
    task_set_ok = 35
    task_done_ok = 36
    task_done_wrong_parameter = 37
    #food
    food_get_wrong_index = 16
    food_get_ok = 17
    food_help = 18
    food_file_broken = 19
    food_ingredient_ok = 32
    #fat
    fat_incorrect_date_format = 20
    fat_delete_success = 21
    fat_delete_incorrect_index = 22
    fat_get_ok = 23
    fat_value_not_given = 24
    fat_add_must_be_float = 25
    fat_added = 26
    #game
    game_get_ok = 27
    game_value_not_given = 28
    game_added = 29
    game_delete_success = 30
    game_delete_incorrect_index = 31
    game_delete_incorrect_name = 38
