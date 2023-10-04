"""
Eric
October 2nd, 2023

Sources:
I used the same BColors class from last time for terminal colors - https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

*THIS VERSION HAS THE EZINPUT LIBRARY IN THE SAME SCRIPT*

Reflection:
This was a nice introduction to 1d lists in python, although this program is called a "grocery_list", it really is just a
list maker that can be used for anything. I also added a quick add feature that allows the user to add multiple items
until they enter the stop keyword. Most methods in this homework are built by accessing elements of a list by its index,
then either modifying or removing it. I also added a feature that allows the user to export the list to a .txt file.

Have a good day! :)

On my honor, I have neither given nor received unauthorized aid on this assignment.
"""

import random
import time
import os
import sys


# All self-built packges shipped here for one-file submission on canvas

# <-----EZInput Package----->
class EZInputHandlerBase:
    def __init__(self):
        self.version = "0.0.1"
        self.author = "Eric Yang'25"
        self.short_term_memory = ""
        self.long_term_memory = []

    # applying while True (try/execpt) for most input types

    def handle_string_input(self, prompt):
        while True:
            try:
                user_input = input(f"{prompt}\n>>>")
                return user_input
            except ValueError:
                print("Invalid input, please try again.")
                return self.handle_string_input(prompt)

    def handle_string_input_no_prompt(self):
        while True:
            try:
                user_input = input("\n>>>")
                return user_input
            except ValueError:
                print("Invalid input, please try again.")
                return self.handle_string_input_no_prompt()

    def handle_int_input(self, prompt):
        while True:
            try:
                user_input = int(input(f"{prompt}\n>>>"))
                return user_input
            except ValueError or TypeError:
                print("Invalid input, please try again.")
                return self.handle_int_input(prompt)

    def handle_float_input(self, prompt):
        while True:
            try:
                user_input = float(input(f"{prompt}\n>>>"))
                return user_input
            except ValueError:
                print("Invalid input, please try again.")
                return self.handle_float_input(prompt)

    def handle_bool_input(self):
        while True:
            try:
                user_input = input("(y/n)\n>>>")
                if user_input.lower().strip() == 'y':
                    return True
                elif user_input.lower().strip() == 'n':
                    return False
            except ValueError:
                print("Invalid input, please try again.")
                return self.handle_bool_input()

    # short and long term memory in case someone needs it(ex remembering player's last interaction)

    def make_short_term_memory(self, memory_item):
        self.short_term_memory = memory_item

    def add_to_long_term_memory(self, memory_item):
        self.long_term_memory.append(memory_item)


# One with usernames you can use/customize
class EZInputHandlerUser(EZInputHandlerBase):
    def __init__(self, username):
        super().__init__()
        self.username = username


# Loading in Bcolors again to get some colors in the terminal without typing every time.
class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def clear_screen():
    '''
    clears terminal screen with multi-os support
    :return: nothing
    '''
    # Using os.system to clear the terminal screen, short if else to support multiple OS
    os.system('cls' if os.name == 'nt' else 'clear')


class ListHandler:
    def __init__(self):
        self.full_list = []
        self.list_name = ""
        self.input_handler = EZInputHandlerBase()

    def add_item(self, item):
        self.full_list.append(item)

    def remove_item(self, item):
        self.full_list.remove(item)

    def remove_item_by_index(self, index):
        self.full_list.pop(index)

    def clear_list(self):
        self.full_list = []

    def print_list(self):
        for i, item in enumerate(self.full_list):
            print(f"{i + 1}. {item}")

    def update_list_name(self, name):
        self.list_name = name

    def update_list_value(self, value, index):
        self.full_list[index] = value

    def create_new_list(self):
        print(f"{BColors.OKGREEN}{BColors.BOLD}What is the name of your list?{BColors.ENDC}{BColors.ENDC}")
        self.list_name = self.input_handler.handle_string_input("Please enter the name of your list")
        self.full_list = []
        print(f"{BColors.OKGREEN}List created.{BColors.ENDC}")

    def user_menu(self):
        print(f"{BColors.OKGREEN}{BColors.BOLD}List Maker V1.0.0{BColors.ENDC}{BColors.ENDC}")
        print(f"{BColors.OKCYAN}1.Create a new list{BColors.ENDC}", end="    ")
        print(f"{BColors.OKCYAN}2.Insert an item to the list{BColors.ENDC}", end="    ")
        print(f"{BColors.OKCYAN}3.Remove an item from the list{BColors.ENDC}", end="\n\n")
        print(f"{BColors.OKCYAN}4.Update a value in the list{BColors.ENDC}", end="    ")
        print(f"{BColors.OKCYAN}5.Clear the list{BColors.ENDC}", end="    ")
        print(f"{BColors.OKCYAN}6.Print the list{BColors.ENDC}", end="\n\n")
        print(f"{BColors.OKCYAN}7.Quick add{BColors.ENDC}", end="    ")
        print(f"{BColors.OKCYAN}8.Export list to .txt{BColors.ENDC}", end="    ")
        print(f"{BColors.OKCYAN}9.Exit{BColors.ENDC}", end="\n\n")

    def quick_add(self):
        print(f"{BColors.BOLD}Use enter to separate your items, type 'STOP' when done.{BColors.ENDC}")
        while True:
            user_input = self.input_handler.handle_string_input_no_prompt()
            if user_input.lower().strip() == 'stop':
                break
            else:
                self.add_item(user_input)

    def export_list(self):
        with open(f"{self.list_name}.txt", "w") as file:
            for item in self.full_list:
                file.write(f"{item}\n")
        print(f"{BColors.OKGREEN}List exported to {self.list_name}.txt{BColors.ENDC}")

    def handle_user_choice(self):
        while True:
            user_input = self.input_handler.handle_int_input("Please enter a number to continue")
            if user_input == 1:
                self.create_new_list()
                break
            elif user_input == 2:
                item = self.input_handler.handle_string_input("Please enter the item you want to add")
                self.add_item(item)
                break
            elif user_input == 3:
                print(f"{BColors.BOLD}Do you want to remove an item by index or by value?{BColors.ENDC}")
                while True:
                    index_or_value = self.input_handler.handle_string_input("Please enter 'index' or 'value'")
                    if index_or_value.lower().strip()[0] == 'i':
                        index = self.input_handler.handle_int_input(
                            "Please enter the index of the item you want to remove")
                        self.remove_item_by_index(index)
                        break
                    elif index_or_value.lower().strip()[0] == 'v':
                        item = self.input_handler.handle_string_input("Please enter the item you want to remove")
                        self.remove_item(item)
                        break
                    else:
                        print("Invalid input, please try again.")
                break
            elif user_input == 4:
                print(f"{BColors.BOLD}Which ith element is the value you want to update?{BColors.ENDC}")
                while True:
                    index = self.input_handler.handle_int_input("Please enter the ith place the value is in")
                    if index > len(self.full_list) or index < 1:
                        print("Invalid input, please try again.")
                    else:
                        print(
                            f"{BColors.BOLD}What do you want to change <{self.full_list[index - 1]}>?{BColors.ENDC}> to?")
                        value = self.input_handler.handle_string_input("Please enter the new value")
                        self.update_list_value(value, index - 1)
                        break
                break
            elif user_input == 5:
                print(f"{BColors.BOLD}Are you sure you want to clear the list?{BColors.ENDC}")
                if self.input_handler.handle_bool_input():
                    self.clear_list()
                    print("List cleared.")
                else:
                    print("List not cleared.")
                break
            elif user_input == 6:
                self.print_list()
                break
            elif user_input == 7:
                self.quick_add()
                break
            elif user_input == 8:
                self.export_list()
                break
            elif user_input == 9:
                os.system('cls' if os.name == 'nt' else 'clear')
                sys.exit()
            else:
                print("Invalid input, please try again.")

    def print_n_elements(self, n):
        for i, item in enumerate(self.full_list):
            if i < n:
                print(f"{i + 1}. {item}")

    def interaction_loop(self):
        clear_screen()
        print(f"{BColors.OKGREEN}{BColors.BOLD}What is the name of your list?{BColors.ENDC}{BColors.ENDC}")
        self.list_name = self.input_handler.handle_string_input("Please enter the name of your list")

        while True:
            clear_screen()
            self.user_menu()
            time.sleep(0.5)
            print("First 10 elements of the list:")
            self.print_n_elements(10)
            print()
            self.handle_user_choice()
            print(f"{BColors.WARNING}{BColors.BOLD}Press enter to continue{BColors.ENDC}")
            input()


if __name__ == "__main__":
    clear_screen()
    list_program = ListHandler()
    list_program.interaction_loop()
