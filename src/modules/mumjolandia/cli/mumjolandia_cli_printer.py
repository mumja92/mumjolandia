import logging
import sys
from src.interface.mumjolandia.mumjolandia_return_value import MumjolandiaReturnValue
from src.utils.polish_utf_to_ascii import PolishUtfToAscii


class MumjolandiaCliPrinter:
    def __init__(self, exit_flag):
        self.views = {}
        self.exit_flag = exit_flag
        self.__init()

    def execute(self, return_value):
        try:
            self.views[return_value.status.name](return_value)
        except KeyError:
            self.views['unrecognized_status_response'](return_value)

    def __init(self):
        self.views['unrecognized_status_response'] = self.view_unrecognized_status_response
        self.views[MumjolandiaReturnValue.mumjolandia_unrecognized_command.name] = self.view_unrecognized_command
        self.views[MumjolandiaReturnValue.mumjolandia_exit.name] = self.view_exit
        self.views[MumjolandiaReturnValue.mumjolandia_unrecognized_parameters.name] = \
            self.view_unrecognized_parameters

        self.views[MumjolandiaReturnValue.task_get.name] = self.view_task_print
        self.views[MumjolandiaReturnValue.task_added.name] = self.view_task_added
        self.views[MumjolandiaReturnValue.task_delete_success.name] = self.view_task_delete_success
        self.views[MumjolandiaReturnValue.task_delete_incorrect_index.name] = self.view_task_delete_incorrect_index
        self.views[MumjolandiaReturnValue.task_delete_incorrect_name.name] = self.view_task_delete_incorrect_name
        self.views[MumjolandiaReturnValue.task_edit_ok.name] = self.view_task_edit_ok
        self.views[MumjolandiaReturnValue.task_edit_wrong_index.name] = self.view_task_edit_wrong_index
        self.views[MumjolandiaReturnValue.task_help.name] = self.view_task_help
        self.views[MumjolandiaReturnValue.task_name_not_given.name] = self.view_task_name_not_given
        self.views[MumjolandiaReturnValue.task_get_wrong_data.name] = self.view_task_get_wrong_data
        self.views[MumjolandiaReturnValue.task_set_ok.name] = self.view_task_set_ok
        self.views[MumjolandiaReturnValue.task_set_incorrect_parameter.name] = self.view_task_set_incorrect_parameter
        self.views[MumjolandiaReturnValue.task_done_ok.name] = self.view_task_done
        self.views[MumjolandiaReturnValue.task_done_wrong_parameter.name] = self.view_task_done_wrong_parameter

        self.views[MumjolandiaReturnValue.food_get_ok.name] = self.view_food_get_ok
        self.views[MumjolandiaReturnValue.food_get_wrong_index.name] = self.view_food_get_wrong_index
        self.views[MumjolandiaReturnValue.food_help.name] = self.view_food_help
        self.views[MumjolandiaReturnValue.food_file_broken.name] = self.view_food_file_broken
        self.views[MumjolandiaReturnValue.food_ingredient_ok.name] = self.view_food_ingredient_ok

        self.views[MumjolandiaReturnValue.fat_get_ok.name] = self.view_fat_get_ok
        self.views[MumjolandiaReturnValue.fat_delete_success.name] = self.view_fat_delete_ok
        self.views[MumjolandiaReturnValue.fat_delete_incorrect_index.name] = self.view_fat_delete_incorrect_index
        self.views[MumjolandiaReturnValue.fat_value_not_given.name] = self.view_fat_value_not_given
        self.views[MumjolandiaReturnValue.fat_add_must_be_float.name] = self.view_fat_add_must_be_float
        self.views[MumjolandiaReturnValue.fat_added.name] = self.view_fat_added

        self.views[MumjolandiaReturnValue.game_value_not_given.name] = self.view_game_value_not_given
        self.views[MumjolandiaReturnValue.game_added.name] = self.view_game_added
        self.views[MumjolandiaReturnValue.game_delete_incorrect_index.name] = self.view_game_delete_incorrect_index
        self.views[MumjolandiaReturnValue.game_delete_incorrect_name] = self.view_game_delete_incorrect_name
        self.views[MumjolandiaReturnValue.game_delete_success.name] = self.view_game_delete_ok
        self.views[MumjolandiaReturnValue.game_get_ok.name] = self.view_game_get_ok

    def view_task_print(self, return_value):
        print(len(return_value.arguments[0]), 'items:')
        for i, t in zip(return_value.arguments[0], return_value.arguments[1]):
            print('[' + str(i) + ']' + str(t))

    def view_task_added(self, return_value):
        print('Added: ' + str(return_value.arguments[0]))

    def view_exit(self, return_value):
        print('exiting')
        self.exit_flag.change(True)

    def view_unrecognized_command(self, return_value):
        print('Unrecognized command: ', return_value.arguments, sep=' ', end='\n', file=sys.stdout, flush=False)

    def view_unrecognized_status_response(self, return_value):
        print('Unrecognized status response: ' + return_value.status.name)
        logging.error("Unrecognized status response: '" + return_value.status.name + "'")

    def view_unrecognized_parameters(self, return_value):
        print("Unrecognized parameters: ",
              return_value.arguments,
              sep=' ',
              end='\n',
              file=sys.stdout,
              flush=False)

    def view_task_delete_success(self, return_value):
        print("Deleted " + return_value.arguments[1] + " element(s) using parameter: " + return_value.arguments[0])

    def view_task_delete_incorrect_index(self, return_value):
        print("Can't delete - incorrect index value: " + return_value.arguments[0])

    def view_task_delete_incorrect_name(self, return_value):
        print("Can't delete - incorrect task name: " + return_value.arguments[0])

    def view_task_edit_ok(self, return_value):
        print("Task edited: " + return_value.arguments[0])

    def view_task_edit_wrong_index(self, return_value):
        print("Edit aborted - wrong index: " + return_value.arguments[0])

    def view_task_help(self, return_value):
        print(return_value.arguments[0])

    def view_task_name_not_given(self, return_value):
        print("Task name not given")

    def view_task_get_wrong_data(self, return_value):
        print("Wrong parameter " + return_value.arguments[0])

    def view_task_set_incorrect_parameter(self, return_value):
        print("Wrong parameters " + str(return_value.arguments))

    def view_task_set_ok(self, return_value):
        print("Set '" + return_value.arguments[0] + "' to " + return_value.arguments[1] + " days ahead")

    def view_task_done(self, return_value):
        print("done")

    def view_task_done_wrong_parameter(self, return_value):
        print("Wrong parameters " + str(return_value.arguments))

    def view_food_get_ok(self, return_value):
        print(PolishUtfToAscii.translate(return_value.arguments[0]))

    def view_food_help(self, return_value):
        print(return_value.arguments[0])

    def view_food_get_wrong_index(self, return_value):
        print('Wrong recipe index: '+return_value.arguments[0])

    def view_food_file_broken(self, return_value):
        print('Database file: "' + return_value.arguments[0] + '" is broken')

    def view_food_ingredient_ok(self, return_value):
        def __view_food_ingredient_ok_print(recipe):
            sorted_list = recipe
            sorted_list.sort()
            for i in sorted_list:
                print(" " + PolishUtfToAscii.translate(i))
        print("\nBreakfast (" + return_value.arguments[0][0] + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[0][1])
        print("\nSecond breakfast (" + return_value.arguments[0][0] + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[1][1])
        print("\nDinner (" + return_value.arguments[0][0] + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[2][1])
        print("\nTea (" + return_value.arguments[0][0] + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[3][1])
        print("\nSupper (" + return_value.arguments[0][0] + "): ")
        __view_food_ingredient_ok_print(return_value.arguments[4][1])
        print("")

    def view_fat_get_ok(self, return_value):
        for i, t in enumerate(return_value.arguments):
            print('[' + str(i) + '] ' + str(t))

    def view_fat_delete_ok(self, return_value):
        print("Deleted " + return_value.arguments[1] + " element(s) using parameter: " + return_value.arguments[0])

    def view_fat_delete_incorrect_index(self, return_value):
        print("Can't delete - incorrect index value: " + return_value.arguments[0])

    def view_fat_value_not_given(self, return_value):
        print("Value not given")

    def view_fat_add_must_be_float(self, return_value):
        print('Parameter must be a number')

    def view_fat_added(self, return_value):
        print('Added: ', return_value.arguments[0])

    def view_game_delete_ok(self, return_value):
        print("Deleted " + return_value.arguments[1] + " element(s) using parameter: " + return_value.arguments[0])

    def view_game_delete_incorrect_index(self, return_value):
        print("Can't delete - incorrect index value: " + return_value.arguments[0])

    def view_game_value_not_given(self, return_value):
        print("Value not given")

    def view_game_delete_incorrect_name(self, return_value):
        print("Can't delete - incorrect name: " + return_value.arguments[0])

    def view_game_added(self, return_value):
        print('Added: ', return_value.arguments[0])

    def view_game_get_ok(self, return_value):
        for i, t in enumerate(return_value.arguments):
            print('[' + str(i) + '] ' + str(t))
