'''
Used ChatGPT for game and rough mechanics idea, although it tried to generate this for a space-themed game.
Used OpenAI company name to make game name
Used ASCII conversion library for display terminal visuals - https://pypi.org/project/image-to-Ascii/
Used Rich text library to style terminal output -
Also used raw color codes for terminal output, the class I used is documented in the code - https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal

I learned about std.flush() from a stackoverflow post a long time ago, but I thought I'd still cite it here - https://stackoverflow.com/questions/20302331/typing-effect-in-python

To really make sure users are paying attention & understanding the rules, I implemented quiz questions throughout
the introduction of the game.

'''

import numpy as np
import random
import time
import math
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
        self.input_handler = EZInputHandlerBase()

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

# <-----start of borrowed color codes from Stack overflow----->
class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# <-----end of borrowed color codes from Stack overflow----->

# Let's first build on the EGame BasicPlayer class to create a unique player class for this game
'''
list of methods in BasicPlayer to quick reference throughout coding:
self.name = player_name
self.health = 100
self.max_health = 100
self.attack = 10
self.defense = 10
self.inventory = []
self.equipped = []
self.xp = 0
self.level = 0
'''


class HackerPlayer(BasicPlayer):
    def __init__(self, player_name):
        super().__init__(player_name)
        self.decryption_skill = 0
        self.intrusion_skill = 0
        self.sys_manipulation_skill = 0

    def set_initial_skills(self, dcypt=0, intr=0, sys_manip=0):
        self.decryption_skill = dcypt
        self.intrusion_skill = intr
        self.sys_manipulation_skill = sys_manip


# let's define a game master class to handle the game's mechanics
class GameMaster:
    def __init__(self, player_object: HackerPlayer):
        self.version = "0.0.1"
        self.input_handler = EZInputHandlerBase()
        self.player = player_object
        self.logs = [
            (f"{Bcolors.OKCYAN}Starting 0Z1...{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKCYAN}Loading configuration files...{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKGREEN}Configurations loaded successfully.{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKCYAN}Establishing connection to database...{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKGREEN}Connection to database established.{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKCYAN}Initializing core modules...{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKGREEN}Core modules initialized successfully.{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKCYAN}Running system checks...{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKGREEN}System checks passed.{Bcolors.ENDC}", 0.12),
            (f"{Bcolors.OKGREEN}0Z1 started successfully.{Bcolors.ENDC}", 0.12),
        ]
        self.loading_sprites = ["|", "/", "-", "\\"]

    def show_loading(self):
        spin_speed = 0.1
        duration = 1
        frames_needed = int(duration / spin_speed)
        for i in range(frames_needed):
            char = self.loading_sprites[i % len(self.loading_sprites)]
            sys.stdout.write('\r' + char + ' Loading...')
            sys.stdout.flush()
            time.sleep(spin_speed)
        print()
    def typewriter_print(self, phrase, color="bright_white", bolded=False):
        phrase = f"{phrase}\n"
        if color == "bright_yellow":
            phrase = f"{Bcolors.WARNING}{phrase}{Bcolors.ENDC}"
        elif color == "bright_red":
            phrase = f"{Bcolors.FAIL}{phrase}{Bcolors.ENDC}"
        elif color == "bright_green":
            phrase = f"{Bcolors.OKGREEN}{phrase}{Bcolors.ENDC}"
        if bolded:
            phrase = f"{Bcolors.BOLD}{phrase}{Bcolors.ENDC}"
        for char in phrase:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.05)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def quiz_rules_int(self, question, ans):
        self.clear_screen()
        self.typewriter_print(question, color="bright_yellow", bolded=True)
        if self.input_handler.handle_int_input("Input your answer here:") == ans:
            self.typewriter_print("Correct!", color="bright_green", bolded=True)
            time.sleep(2)
            return True
        else:
            self.typewriter_print("Incorrect, PAY ATTENTION, this game is not for the light-minded.",
                                  color="bright_red", bolded=True)
            time.sleep(2)
            return False

    def setup_game(self):
        self.clear_screen()
        for log, delay in self.logs:
            print(log)
            time.sleep(delay)
        self.show_loading()
        self.typewriter_print("Username: 0Z1")
        self.typewriter_print("Access Code: *********")
        time.sleep(1)
        self.clear_screen()
        print(f"{Bcolors.OKGREEN}<--------Connected to datacenter 01 :: 23.231.323.68--------->{Bcolors.ENDC}")
        time.sleep(2)
        self.typewriter_print("Ok, we're in the first datacenter...let's throw a tester program in first",
                              color="bright_yellow")
        self.show_loading()
        print(f"{Bcolors.FAIL}{Bcolors.BOLD}Error: No Scripts Available{Bcolors.ENDC}{Bcolors.ENDC}")
        time.sleep(1.2)
        self.typewriter_print("Oops, we didn't ship the dummy with any hacking scripts...",
                              color="bright_yellow")
        time.sleep(1.2)
        self.typewriter_print("Hacking scripts are type-specific and one-time use",
                              color="bright_yellow")
        time.sleep(1.2)
        self.typewriter_print("There are three type of scripts: 1. Decryption, 2. Intrusion, 3. Sys-Manipulation",
                              color="bright_yellow")
        time.sleep(1.2)
        self.typewriter_print("If you run out of scripts, you can't hack that type until you collect more.",
                              color="bright_yellow")
        time.sleep(1.2)
        self.typewriter_print("Look for resource stations in datacenters to get more scripts",
                              color="bright_red", bolded=True)
        time.sleep(3)
        while True:
            self.clear_screen()
            print(f"{Bcolors.OKGREEN}<--------Connected to datacenter 01 :: 23.231.323.68--------->{Bcolors.ENDC}")
            self.typewriter_print("We'll give you 10 scripts to start, split it between the three categories",
                                  color="bright_yellow", bolded=True)
            time.sleep(1.6)
            self.typewriter_print("For example: 3 Decryption, 4 Intrusion, 3 Sys-manipulation",
                                  color="bright_yellow", bolded=True)
            time.sleep(3)
            decryption_assign = self.input_handler.handle_int_input("How many scripts do you want for Decryption?")
            intrusion_assign = self.input_handler.handle_int_input("How many scripts do you want for Intrusion?")
            sys_assign = self.input_handler.handle_int_input("How many scripts do you want for System Manipulation?")
            if decryption_assign + intrusion_assign + sys_assign == 10:
                break
            else:
                self.typewriter_print("Good try, but we caught that! Re-enter your values", color="bright_red", bolded=True)
                time.sleep(2)
        self.typewriter_print("Alright, lets restart the connection...", color="bright_yellow", bolded=True)
        self.show_loading()
        self.player.set_initial_skills(decryption_assign, intrusion_assign, sys_assign)
        self.play_game()
    def play_game(self):
        pass
    def introduce_game(self):
        self.clear_screen()
        self.typewriter_print("It's currently the year 2050, an evil AI mega corporation called ClosedAI is "
                              "controlling entire cybernetic cities.")
        time.sleep(3)
        self.clear_screen()
        self.typewriter_print("Everyone in this city depends on their AI model called JPT.")
        time.sleep(2)
        self.typewriter_print("This model brainwashes its users and makes people dumber everyday...",
                              color="bright_red", bolded=True)
        time.sleep(3)
        self.clear_screen()
        self.typewriter_print("Oh...sorry. I didn't introduce myself.......")
        time.sleep(2)
        self.typewriter_print("Well I can't exactly tell you who I am...I'm from the organization")
        time.sleep(2)
        self.typewriter_print("But we do know a lot about you...like how you've been locked up for the last 20 years",
                              color="bright_red")
        time.sleep(2)
        self.typewriter_print("You still have 30 years before your prison sentence is over...")
        time.sleep(2)
        self.clear_screen()
        self.typewriter_print("Oh...you don't remember what you did? 20 years in solitary confinement sure did a lot!")
        time.sleep(2)
        self.typewriter_print("Well, what you did was horrible, all I can say is that it was related to hacking...")
        time.sleep(2)
        self.typewriter_print("Today, you have an opportunity. If you manage to hack ClosedAI, you sentence will end.",
                              color="bright_red", bolded=True)
        time.sleep(3)
        self.typewriter_print("You must hack into their system and destroy their AI model.",
                              color="bright_yellow", bolded=True)
        time.sleep(1)
        self.typewriter_print("Do you understand your mission?", color="bright_yellow", bolded=True)
        if not self.input_handler.handle_bool_input():
            self.typewriter_print("You must understand your mission to continue.", color="bright_red", bolded=True)
            self.introduce_game()
        while True:
            self.clear_screen()
            self.typewriter_print("Hacking ClosedAI is no easy task", color="bright_yellow", bolded=True)
            time.sleep(2)
            self.typewriter_print("ClosedAI hides it's AI behind an encrypted firewall.", color="bright_red",
                                  bolded=True)
            time.sleep(2)
            self.typewriter_print(f"To break the wall, you'll need its {Bcolors.BOLD}encryption key{Bcolors.ENDC}.")
            time.sleep(2)
            self.typewriter_print("The key is a 5 digit number.", color="bright_yellow", bolded=True)
            time.sleep(2)
            if self.quiz_rules_int("How many digits is the encryption key to hack ClosedAI?", 5):
                break
        while True:
            self.clear_screen()
            self.typewriter_print(
                f"ClosedAI leaves each digit of the {Bcolors.BOLD}encryption key{Bcolors.ENDC} in a random datacenter.")
            time.sleep(2)
            self.typewriter_print("The organization has found these 5 datacenters for you")
            time.sleep(2)
            self.clear_screen()
            self.typewriter_print("In each datacenter, you objective is to find vulnerabilities in individual servers")
            time.sleep(2)
            self.typewriter_print(f"Once you found it, {Bcolors.BOLD}EXPLOIT IT{Bcolors.ENDC}", color="bright_red")
            time.sleep(3)
            self.typewriter_print("When you've exploited all vulnerabilities, find and log in to the terminal.",
                                  color="bright_yellow")
            time.sleep(2)
            self.typewriter_print("You probably want to write down what the terminal says", color="bright_red",
                                  bolded=True)
            time.sleep(2)
            if self.quiz_rules_int("How many datacenters do you need to hack to fully decrypt the key?", 5):
                break
        self.clear_screen()
        self.typewriter_print("Are you ready to hack?", color="bright_yellow", bolded=True)
        if self.input_handler.handle_bool_input():
            self.setup_game()
        else:
            self.typewriter_print("Ok, good luck with 30 more years in jail. Goodbye.", color="bright_red", bolded=True)
            self.clear_screen()

    def generate_floor(self, with_security=False, with_portal=False):
        '''
        -1 = get a skill/move up down, 0 = empty, 1 = decryption, 2 = intrusion, 3 = manipulation, 4 antivirus,
        5 = terminal (give digit when all auth tasks complete), 6 firewall portal (fifth floor only)
        '''
        floor_grid = np.zeros((9, 9), dtype=int)
        gen_vals = [1, 2, 3, 4]
        for val in gen_vals:
            count = 0
            while count < 3:
                rand_row = random.randint(0, 8)
                rand_col = random.randint(0, 8)
                if floor_grid[rand_row][rand_col] == 0:
                    floor_grid[rand_row][rand_col] = val
                    count += 1
        skill_add_count = 0
        while skill_add_count < 6:
            rand_row = random.randint(0, 8)
            rand_col = random.randint(0, 8)
            if floor_grid[rand_row][rand_col] == 0:
                floor_grid[rand_row][rand_col] = -1
                skill_add_count += 1
        if with_security:
            security_count = 0
            while security_count < 1:
                rand_row = random.randint(0, 8)
                rand_col = random.randint(0, 8)
                if floor_grid[rand_row][rand_col] == 0:
                    floor_grid[rand_row][rand_col] = 4
                    security_count += 1
        if with_portal:
            portal_count = 0
            while portal_count < 1:
                rand_row = random.randint(0, 8)
                rand_col = random.randint(0, 8)
                if floor_grid[rand_row][rand_col] == 0:
                    floor_grid[rand_row][rand_col] = 6
                    portal_count += 1
        else:
            terminal_count = 0
            while terminal_count < 1:
                rand_row = random.randint(0, 8)
                rand_col = random.randint(0, 8)
                if floor_grid[rand_row][rand_col] == 0:
                    floor_grid[rand_row][rand_col] = 5
                    terminal_count += 1

        # <--------TESTING CODE---------->
        # for i in range(len(floor_grid)):
        #     for j in range(len(floor_grid[i])):
        #         print(floor_grid[i][j], end=" ")
        #     print()
        return floor_grid


if __name__ == "__main__":
    # using different clears so this works on more platforms
    # os.system('cls' if os.name == 'nt' else 'clear')
    # while True:
    #     try:
    #         name = input("Pick a cool hacker name!\n>>>")
    #         break
    #     except ValueError and TypeError:
    #         print("Invalid input, try again.")
    #
    # player = HackerPlayer(name)
    # game_master = GameMaster(player)
    # time.sleep(0.5)
    # game_master.introduce_game()

    # <------testing code(DO NOT RUN)------------>
    test_player = HackerPlayer("Eric")
    test_game_master = GameMaster(test_player)
    test_game_master.setup_game()
