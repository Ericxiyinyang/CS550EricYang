'''
Used ChatGPT for game and rough mechanics idea, although it tried to generate this for a space-themed game.
Used OpenAI company name to make game name
Used ASCII conversion library for display terminal visuals - https://pypi.org/project/image-to-Ascii/
Used Rich text library to style terminal output
'''

import numpy
import random
import time
import math
import os
from rich import print as rprint


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


# <-----EGame Package----->
class BasicPlayer:
    def __init__(self, player_name):
        self.version = "0.0.1"
        self.author = "Eric Yang'25"
        self.name = player_name
        self.health = 100
        self.max_health = 100
        self.attack = 10
        self.defense = 10
        self.inventory = []
        self.equipped = []
        self.xp = 0
        self.level = 0
        self.input_handler = EZInputHandlerBase

    def get_player_name(self):
        return self.name

    def get_health(self):
        return self.health

    def get_max_health(self):
        return self.max_health

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_inventory(self):
        return self.inventory

    def get_equipped(self):
        return self.equipped

    def get_xp(self):
        return self.xp

    def get_level(self):
        return self.level

    def set_player_name(self, new_name):
        self.name = new_name

    def set_health(self, new_health):
        self.health = new_health

    def set_max_health(self, new_max_health):
        self.max_health = new_max_health

    def set_attack(self, new_attack):
        self.attack = new_attack

    def set_defense(self, new_defense):
        self.defense = new_defense

    def set_inventory(self, new_inventory):
        self.inventory = new_inventory

    def add_to_inventory(self, new_item):
        self.inventory.append(new_item)

    def set_equipped(self, new_equipped):
        self.equipped = new_equipped

    def add_to_equipped(self, new_equipped):
        self.equipped.append(new_equipped)

    def set_xp(self, new_xp):
        self.xp = new_xp

    def set_level(self, new_level):
        self.level = new_level

    def add_xp(self, xp_gained):
        self.xp += xp_gained
        if self.xp >= 100:
            self.level += 1
            self.xp = 0


# <-----Start of game code----->

# Let's first build on the EGame BasicPlayer class to create a unique player class for this game

class HackerPlayer(BasicPlayer):
    def __init__(self, player_name):
        super().__init__(player_name)
        self.decryption_skill = 0
        self.intrusion_skill = 0
        self.sys_manipulation_skill = 0

    def set_skills(self):
        pass


# let's define a game master class to handle the game's mechanics
class GameMaster:
    def __init__(self):
        self.version = "0.0.1"
        self.input_handler = EZInputHandlerBase

    def introduce_game(self):
        print("Welcome to the game!")
        time.sleep(1)
        player_name = self.input_handler.handle_string_input("What is your name?")
        return player_name


if __name__ == "__main__":
    game_master = GameMaster()
    player = game_master.introduce_game()
    player_object = HackerPlayer(player)
