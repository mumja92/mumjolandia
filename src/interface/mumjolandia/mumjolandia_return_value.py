from enum import Enum, unique


@unique
class MumjolandiaReturnValue(Enum):
    mumjolandia_none = 0
    mumjolandia_unrecognized_parameters = 11
    mumjolandia_unrecognized_command = 2
    mumjolandia_exit = 9
    mumjolandia_help = 45
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
    task_undone_ok = 67
    task_done_wrong_parameter = 37
    task_bump_ok = 73
    task_bump_nook = 74
    task_find = 76
    # food
    food_get_wrong_index = 16
    food_get_ok = 17
    food_help = 18
    food_file_broken = 19
    food_ingredient_ok = 32
    # fat
    fat_incorrect_date_format = 20
    fat_delete_success = 21
    fat_delete_incorrect_index = 22
    fat_get_ok = 23
    fat_value_not_given = 24
    fat_add_must_be_float = 25
    fat_added = 26
    # game
    game_get_ok = 27
    game_value_not_given = 28
    game_added = 29
    game_exist = 38
    game_delete_success = 30
    game_delete_incorrect_index = 31
    game_help = 46
    game_current_get = 55
    game_set_ok = 56
    game_set_wrong_id = 57
    # note
    note_add_ok = 39
    note_add_nook = 44
    note_help = 40
    note_get_ok = 41
    note_delete_success = 42
    note_delete_incorrect_index = 43
    # connection
    connection_help = 47
    connection_server_start = 52
    connection_client_send_ok = 51
    connection_failed = 54
    # game
    event_get_ok = 48
    event_help = 49
    # weather
    weather_get_ok = 50
    weather_get_nook = 53
    weather_help = 58
    # password
    password_set_ok = 59
    password_set_incorrect = 60
    password_incorrect_value = 61
    password_not_set = 62
    password_get_ok = 63
    password_list_ok = 64
    password_help = 65
    password_add_ok = 66
    password_rm_ok = 68

    pompejanka_message = 71

    cli_handled = 69
    cli_mode = 72

    utils_help = 70
    utils_get = 75
    utils_shared_preferences_get = 77
