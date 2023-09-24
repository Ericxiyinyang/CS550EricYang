'''
Used ChatGPT for game and rough mechanics idea, although it tried to generate this for a space-themed game.
Used OpenAI company name to make game name
Used ASCII conversion library for display terminal visuals - https://pypi.org/project/image-to-Ascii/
Used Rich text library to style terminal output -
Also used raw color codes for terminal output, the class I used is documented in the code - https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
Used "Ericsweeper" that I built previously and modified it to be a "system manipulation" game


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
        self.health = 3
        self.max_health = 3
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
        self.decryption_skill = 3
        self.intrusion_skill = 3
        self.sys_manipulation_skill = 4

    def set_initial_skills(self, dcypt=0, intr=0, sys_manip=0):
        self.decryption_skill = dcypt
        self.intrusion_skill = intr
        self.sys_manipulation_skill = sys_manip


# let's define a game master class to handle the game's mechanics
class GameMaster:
    def __init__(self, player_object: HackerPlayer, skip_intro=False):
        self.skip_intro = skip_intro
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
        self.server_floors = []
        self.decryption_key = 0
        self.server_ips = ["22.561.469.69", "99.203.031.12", "78.905.203.11", "23.434.902.22", "69.420.981.21"]
        self.current_row = 0
        self.current_col = 0
        self.current_floor = 0
        self.on_terminal = False
        self.on_portal = False
        self.on_corrupt = False
        self.on_security = False
        self.on_empty = False
        self.on_decryption = False
        self.on_intrusion = False
        self.on_sys_manipulation = False
        self.decryption_tasks_left = 0
        self.intrusion_tasks_left = 0
        self.sys_manipulation_tasks_left = 0
        self.game_won = False
        self.python_questions = [
            "How do you print 'Hello, World!'?",
            "How do you concatenate the strings 'Python' and 'Rocks'?",
            "How do you find the length of the string 'Python'?",
            "How do you convert the integer 123 to a string?",
            "How do you get the last element of the list [1, 2, 3, 4, 5]?",
            "How do you reverse the list [1, 2, 3, 4, 5]?",
            "How do you get the unique elements of the list [1, 1, 2, 2, 3, 3]?",
            "How do you check if the string 'Python' contains the character 'y'?",
            "How do you convert the string '123' to an integer?",
            "How do you round the float 123.456 to 2 decimal places?",
            "How do you get the ASCII value of the character 'A'?",
            "How do you get the character representation of the ASCII value 97?",
            "How do you compute 5 raised to the power of 3?",
            "How do you check if the number 5 is even or odd?",
            "How do you get the remainder when 9 is divided by 4?",
            "How do you get a list of all keys in the dictionary {'a': 1, 'b': 2, 'c': 3}?",
            "How do you get a list of all values in the dictionary {'a': 1, 'b': 2, 'c': 3}?",
            "How do you convert a list [1, 2, 3, 4, 5] to a tuple?",
            "How do you get the maximum value from the list [1, 2, 3, 4, 5]?",
            "How do you get the minimum value from the list [1, 2, 3, 4, 5]?",
            "How do you sum all elements in the list [1, 2, 3, 4, 5]?",
            "How do you get the average of the list [1, 2, 3, 4, 5]?",
            "How do you check if the number 7 is in the list [1, 2, 3, 4, 5]?",
            "How do you get the index of the element 3 in the list [1, 2, 3, 4, 5]?",
            "How do you repeat the string 'Python' 3 times?",
            "How do you convert the tuple (1, 2, 3, 4, 5) to a list?",
            "How do you check if the variable x is of the type integer?",
            "How do you get the absolute value of -123?",
            "How do you check if two strings 'abc' and 'cba' are anagrams?",
            "How do you swap the values of two variables a and b?"
        ]
        self.python_questions_ans = [
            'print("Hello, World!")',
            "'Python' + 'Rocks'",
            "len('Python')",
            "str(123)",
            "[1, 2, 3, 4, 5][-1]",
            "[1, 2, 3, 4, 5][::-1]",
            "set([1, 1, 2, 2, 3, 3])",
            "'y' in 'Python'",
            "int('123')",
            "round(123.456, 2)",
            "ord('A')",
            "chr(97)",
            "5 ** 3",
            "5 % 2 != 0",
            "9 % 4",
            "{'a': 1, 'b': 2, 'c': 3}.keys()",
            "{'a': 1, 'b': 2, 'c': 3}.values()",
            "tuple([1, 2, 3, 4, 5])",
            "max([1, 2, 3, 4, 5])",
            "min([1, 2, 3, 4, 5])",
            "sum([1, 2, 3, 4, 5])",
            "sum([1, 2, 3, 4, 5]) / len([1, 2, 3, 4, 5])",
            "7 in [1, 2, 3, 4, 5]",
            "[1, 2, 3, 4, 5].index(3)",
            "'Python' * 3",
            "list((1, 2, 3, 4, 5))",
            "isinstance(x, int)",
            "abs(-123)",
            "sorted('abc') == sorted('cba')",
            "a, b = b, a"
        ]
        self.number_riddles = [
            "I am a number, one less than a dozen. Who am I?",
            "If you have three quarters, a dime, and two pennies, how much money do you have in total?",
            "I am the number of days in a fortnight. What number am I?",
            "I am the number of fingers you have. What am I?",
            "The number of months in a year is?",
            "I am a number that rhymes with 'heaven'. What am I?",
            "If you have two nickels and three pennies, how much money do you have in total?",
            "I am the smallest two-digit prime number. Who am I?",
            "I am a number that is three more than twenty. What am I?",
            "I am the number of hours in a day. Who am I?",
            "When you add the number of legs a tripod has to the number of sides a triangle has, what do you get?",
            "I am the number of years in a decade. Who am I?",
            "I am the number that represents a perfect score in bowling. Who am I?",
            "I am a number, and when you add 4 to me, you get 20. Who am I?",
            "I am a number, the square root of eighty-one. What number am I?",
            "If you multiply the number of eyes a human has by the number of fingers in a hand, what number do you get?",
            "I am a number, the sum of the angles in a triangle in degrees. Who am I?",
            "I am a number between six and eight. Who am I?",
            "I am a number, the age you are considered an adult in many countries. Who am I?",
            "I am the number of points a snowflake traditionally has. What am I?",
            "I am a number, the product of seven and three. Who am I?",
            "I am a number, and when you subtract 5 from me, you get 15. Who am I?",
            "I am a number, and I represent a golden year. Who am I?",
            "I am a number, and when you add 1 to me, you get a dozen. Who am I?",
            "I am a number, and I am the number of letters in the English alphabet. Who am I?",
            "If you have two dimes and a nickel, how much money do you have in total?",
            "I am the number of weeks in half a year. Who am I?",
            "I am a number, and I am the age you can start to drive a car in many countries. Who am I?",
            "I am a number, and I am the highest single-digit number. Who am I?",
            "I am the number of degrees in a right angle. Who am I?"
        ]
        self.number_riddles_ans = [
            11,
            97,
            14,
            10,
            12,
            7,
            13,
            11,
            23,
            24,
            6,
            10,
            300,
            16,
            9,
            10,
            180,
            7,
            18,
            6,
            21,
            20,
            50,
            11,
            26,
            25,
            26,
            16,
            9,
            90
        ]
        self.server_connect_logs_BefS = [
            (f"{Bcolors.OKCYAN}Initializing system...{Bcolors.ENDC}", 0.2),
            (f"{Bcolors.OKCYAN}Connecting to server...{Bcolors.ENDC}", 0.2)
        ]
        self.server_connect_logs_AftS = [
            (f"{Bcolors.OKGREEN}Secure connection established.{Bcolors.ENDC}", 0.2),
            (f"{Bcolors.OKCYAN}Fetching data from server...{Bcolors.ENDC}", 0.2),
            (f"{Bcolors.OKGREEN}Data fetched successfully.{Bcolors.ENDC}", 0.2),
        ]
        self.sweep_board = np.zeros((10, 10))
        self.sweep_board = np.zeros((10, 10), int)
        for i in range(len(self.sweep_board)):
            for j in range(len(self.sweep_board[i])):
                self.sweep_board[i][j] = random.randint(0, 1)
        rand_row = random.randint(0, 9)
        rand_col = random.randint(0, 9)
        self.sweep_board[rand_row][rand_col] = 2


    def show_loading(self, text="Loading..."):
        spin_speed = 0.1
        duration = 1
        frames_needed = int(duration / spin_speed)
        for i in range(frames_needed):
            char = self.loading_sprites[i % len(self.loading_sprites)]
            sys.stdout.write('\r' + char + text)
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
        if self.skip_intro is False:
            for log, delay in self.logs:
                print(log)
                time.sleep(delay)
            self.show_loading()
            self.typewriter_print("Username: 0Z1")
            self.typewriter_print("Access Code: *********")
            time.sleep(1)
            self.clear_screen()
            print(f"{Bcolors.OKGREEN}<--------Connected to datacenter 01 :: {self.server_ips[0]}--------->{Bcolors.ENDC}")
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
            print(
                f"{Bcolors.OKGREEN}<--------Connected to datacenter 01 :: {self.server_ips[0]}--------->{Bcolors.ENDC}")
            self.typewriter_print("We'll give you 10 scripts to start, split it between the three categories",
                                  color="bright_yellow", bolded=True)
            time.sleep(1)
            self.typewriter_print("For example: 3 Decryption, 4 Intrusion, 3 Sys-manipulation",
                                  color="bright_yellow", bolded=True)
            time.sleep(0.3)
            decryption_assign = self.input_handler.handle_int_input("How many scripts do you want for Decryption?")
            intrusion_assign = self.input_handler.handle_int_input("How many scripts do you want for Intrusion?")
            sys_assign = self.input_handler.handle_int_input("How many scripts do you want for System Manipulation?")
            break
            # ENABLE CODE BELOW WHEn NOT TESTING
            # if decryption_assign + intrusion_assign + sys_assign == 10:
            #     break
            # else:
            #     self.typewriter_print("Good try, but we caught that! Re-enter your values", color="bright_red",
            #                           bolded=True)
            #     time.sleep(2)
        self.typewriter_print("Alright, lets restart the connection...", color="bright_yellow", bolded=True)
        self.show_loading()
        self.player.set_initial_skills(decryption_assign, intrusion_assign, sys_assign)
        game_stat = self.play_game()
        if game_stat:
            self.typewriter_print("You did it! You hacked the AI and got the decryption key!", color="bright_yellow",
                                  bolded=True)
            time.sleep(2)
            self.typewriter_print("You prison sentence has been lifted effective today", bolded=True)
            time.sleep(2)
            self.typewriter_print("You are now free to go", bolded=True)
            self.clear_screen()
            self.typewriter_print(f"Thank you for playing {self.player.name}", color="bright_yellow", bolded=True)
            time.sleep(2)
            self.typewriter_print(
                "This game was made by Eric Yang'25, with plenty of coughs and fevers along the way :)",
                color="bright_yellow", bolded=True)
            time.sleep(2)
            self.typewriter_print("I hope you enjoyed it!", color="bright_yellow", bolded=True)
            time.sleep(2)
            self.typewriter_print("Goodbye!", color="bright_yellow", bolded=True)
            time.sleep(2)
            self.clear_screen()
        else:
            self.typewriter_print("You failed to hack the AI and got caught", color="bright_yellow", bolded=True)
            time.sleep(2)
            self.typewriter_print("You have been sentenced to 30 more years in prison", color="bright_yellow",
                                  bolded=True)
            time.sleep(2)
            self.typewriter_print("Better luck next time", color="bright_yellow", bolded=True)
            time.sleep(2)
            self.typewriter_print("Goodbye!", color="bright_yellow", bolded=True)
            time.sleep(2)
            self.clear_screen()
        self.typewriter_print("Play again?")
        if self.input_handler.handle_bool_input():
            self.clear_screen()
            while True:
                try:
                    name = input("Enter your name!\n>>>")
                    break
                except ValueError and TypeError:
                    print("Invalid input, try again.")
            self.player.set_player_name(name)
            time.sleep(0.5)
            self.introduce_game()
        else:
            print("Goodbye :)")
            time.sleep(1)
            self.clear_screen()

    def print_fake_logs(self, logs_in):
        for log, delay in logs_in:
            print(log)
            time.sleep(delay)

    def play_game(self):
        self.clear_screen()
        self.print_fake_logs(self.logs)
        self.show_loading()
        self.clear_screen()
        for i in range(2):
            self.server_floors.append(self.generate_floor(with_security=True))
        self.server_floors.append(self.generate_floor(with_security=True, with_portal=True))
        self.decryption_key = random.randint(100, 999)
        game_over = self.play_floor(0)
        while game_over is False:
            self.clear_screen()
            self.typewriter_print(
                f"{Bcolors.OKGREEN}You've hacked this data center successfully, moving on to the next one...{Bcolors.ENDC}",
                bolded=True)
            self.show_loading()
            self.clear_screen()
            self.current_floor += 1
            game_over = self.play_floor(self.current_floor)
            if self.game_won:
                return True
        return False

    def hack_menu(self):
        self.set_current_conditions()
        print(f"{Bcolors.OKGREEN}Hacking tools V1.0.2: West Region build{Bcolors.ENDC}")
        print(
            f"Decryption: {self.player.decryption_skill} | Intrusion: {self.player.intrusion_skill} | Sys: {self.player.sys_manipulation_skill}")
        print(
            f"{Bcolors.WARNING}Vulnerabilities left to exploit: {self.decryption_tasks_left} decryption, {self.intrusion_tasks_left} intrusion, {self.sys_manipulation_tasks_left} sys-manipulation{Bcolors.ENDC}")
        time.sleep(1)
        print()
        if self.on_corrupt:
            print("<!!!!!!!Corrupt Server Found!!!!!!!->")
            time.sleep(1)
            print("1: Get 1 decryption script", "2: Get 1 intrusion script", "3: Get 1 sys script",
                  "4: Get 1 antivirus protection")
            while True:
                action = self.input_handler.handle_int_input("Please enter desired action:")
                if action == 1:
                    self.player.decryption_skill += 1
                    print("1 decryption script added")
                    break
                elif action == 2:
                    self.player.intrusion_skill += 1
                    print("1 intrusion script added")
                    break
                elif action == 3:
                    self.player.sys_manipulation_skill += 1
                    print("1 sys manipulation script added")
                    break
                elif action == 4:
                    self.player.health += 1
                    print("1 antivirus protection added")
                    break
                else:
                    print("Invalid action")
            return "Corrupt"

        elif self.on_empty:
            print(f"{Bcolors.FAIL}<--------Empty Server Error: NO DATA-------->{Bcolors.ENDC}")
            return "Empty"
        elif self.on_decryption:
            print("<!!!!!!!Decryption Vulnerability Found!!!!!!!>")
            time.sleep(1)
            if self.player.decryption_skill > 0:
                print("0: Do nothing, 1: Exploit vulnerability")
                while True:
                    action = self.input_handler.handle_int_input("Please enter desired action:")
                    if action == 1:
                        self.player.decryption_skill -= 1
                        decrypted = self.play_decryption()
                        if decrypted:
                            self.decryption_tasks_left -= 1
                            self.on_decryption = False
                            print(f"{Bcolors.OKGREEN}{Bcolors.BOLD}Vulnerability exploited{Bcolors.ENDC}{Bcolors.ENDC}")
                            self.server_floors[self.current_floor][self.current_row][self.current_col] = 0
                            return "Decrypted"
                        else:
                            print(f"{Bcolors.FAIL}Failed to exploit...try again later{Bcolors.ENDC}")
                            break
                    elif action == 0:
                        break
                    else:
                        print("Invalid action")
            else:
                print(f"{Bcolors.FAIL}You don't have any decryption scripts{Bcolors.ENDC}")
            return "Not Decrypted"



        elif self.on_intrusion:
            print("<!!!!!!!Intrusion Vulnerability Found!!!!!!!>")
            time.sleep(1)
            if self.player.intrusion_skill > 0:
                print("0: Do Nothing, 1: Exploit vulnerability")
                while True:
                    action = self.input_handler.handle_int_input("Please enter desired action:")
                    if action == 1:
                        self.player.intrusion_skill -= 1
                        intruded = self.play_intrusion()
                        if intruded:
                            self.intrusion_tasks_left -= 1
                            self.on_intrusion = False
                            print(f"{Bcolors.OKGREEN}{Bcolors.BOLD}Vulnerability exploited{Bcolors.ENDC}{Bcolors.ENDC}")
                            self.server_floors[self.current_floor][self.current_row][self.current_col] = 0
                            return "Intruded"
                        else:
                            print(f"{Bcolors.FAIL}Failed to exploit...try again later{Bcolors.ENDC}")
                            break
                    elif action == 0:
                        break
                    else:
                        print("Invalid action")
            else:
                print(f"{Bcolors.FAIL}You don't have any intrusion scripts{Bcolors.ENDC}")
            return "Not Intruded"
        elif self.on_sys_manipulation:
            print("<!!!!!!!System Manipulation Vulnerability Found!!!!!!!>")
            time.sleep(1)
            if self.player.sys_manipulation_skill > 0:
                print("0: Do Nothing, 1: Exploit vulnerability")
                while True:
                    action = self.input_handler.handle_int_input("Please enter desired action:")
                    if action == 1:
                        self.player.sys_manipulation_skill -= 1
                        maniped = self.play_sys_manip()
                        if maniped:
                            self.sys_manipulation_tasks_left -= 1
                            self.on_sys_manipulation = False
                            print(f"{Bcolors.OKGREEN}{Bcolors.BOLD}Vulnerability exploited{Bcolors.ENDC}{Bcolors.ENDC}")
                            self.server_floors[self.current_floor][self.current_row][self.current_col] = 0
                            return "Manipulated"
                        else:
                            print(f"{Bcolors.FAIL}Failed to exploit...try again later{Bcolors.ENDC}")
                            break
                    elif action == 0:
                        break
                    else:
                        print("Invalid action")
            else:
                print(f"{Bcolors.FAIL}You don't have any sys-manipulation scripts{Bcolors.ENDC}")
            return "Not Manipulated"
        elif self.on_terminal:
            print("<!!!!!!!Terminal Found!!!!!!!>")
            time.sleep(1)
            if self.decryption_tasks_left == 0 and self.intrusion_tasks_left == 0 and self.sys_manipulation_tasks_left == 0:
                print("1: Log in to terminal")
                action = self.input_handler.handle_int_input("Please enter desired action:")
                while True:
                    if action == 1 and self.current_floor < 2:
                        self.play_terminal()
                        return "Floor Completed"
                    elif action == 1 and self.current_floor == 2:
                        self.play_terminal()
                        return "Last Floor Terminal"
                    else:
                        print("Invalid action")
                        action = self.input_handler.handle_int_input("Please enter desired action:")
            else:
                print(f"{Bcolors.FAIL}Auth Fail: No Terminal Access{Bcolors.ENDC}")
                print(f"{Bcolors.WARNING}(HINT) Complete all hacking vulnerabilities{Bcolors.ENDC}")
                time.sleep(1)
                return "Floor Not Completed"
        elif self.on_security:
            print(f"{Bcolors.FAIL}{Bcolors.BOLD}>>>Antivirus Triggered<<<{Bcolors.ENDC}{Bcolors.ENDC}")
            time.sleep(1)
            if self.player.health == 0:
                self.clear_screen()
                print(f"{Bcolors.FAIL}{Bcolors.BOLD}>>>Program Terminated<<<{Bcolors.ENDC}{Bcolors.ENDC}")
                time.sleep(2)
                return "Terminated"
            self.player.health -= 1
            if self.player.health > 0:
                print(f"{Bcolors.FAIL}You can only trigger the antivirus {self.player.health} more times{Bcolors.ENDC}")
            else:
                print(
                    f"{Bcolors.FAIL}WATCH OUT, your program will TERMINATE the next time if you don't pickup a shield{Bcolors.ENDC}")
        elif self.on_portal:
            print("<!!!!!!!Target Decryption Portal Found!!!!!!!>")
            time.sleep(1)
            print(f"{Bcolors.FAIL}{Bcolors.BOLD}>>>Warning: You have ONE try to enter the decryption key<<<{Bcolors.ENDC}{Bcolors.ENDC}")
            print("0: Do Nothing, 1: Enter full decryption key to portal")
            while True:
                action = self.input_handler.handle_int_input("Please enter desired action:")
                if action == 1:
                    self.game_won = self.play_portal()
                    if self.game_won:
                        return "Game Won"
                    else:
                        print(f"{Bcolors.FAIL}You failed to decrypt the AI{Bcolors.ENDC}")
                        return "Portal Fail"
                elif action == 0:
                    break
                else:
                    print("Invalid action")

        time.sleep(2)
        # ------------------------------------------------------

    def move_player(self):
        self.clear_screen()
        print(
            f"{Bcolors.WARNING}{Bcolors.BOLD}<--------Connected to datacenter 0{self.current_floor + 1} :: Server[row:{self.current_row + 1}, col:{self.current_col + 1}] ::{self.server_ips[self.current_floor - 1]}--------->{Bcolors.ENDC}{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}Hacking tools V1.0.2: West Region build{Bcolors.ENDC}")
        print(
            f"Decryption: {self.player.decryption_skill} | Intrusion: {self.player.intrusion_skill} | Sys: {self.player.sys_manipulation_skill}")
        print(
            f"{Bcolors.WARNING}Vulnerabilities left to exploit: {self.decryption_tasks_left} decryption, {self.intrusion_tasks_left} intrusion, {self.sys_manipulation_tasks_left} sys-manipulation{Bcolors.ENDC}")
        print()
        if self.current_row != 0:
            print("W: Move Forward", end=" ")
        if self.current_row != 8:
            print("S: Move Backward", end=" ")
        if self.current_col != 0:
            print("A: Move Left", end=" ")
        if self.current_col != 8:
            print("D: Move Right", end=" ")
        print()
        print()
        while True:
            direction = self.input_handler.handle_string_input("Please enter desired action:")
            if direction.lower().strip() == "w" and self.current_row != 0:
                self.current_row -= 1
                break
            elif direction.lower().strip() == "s" and self.current_row != 8:
                self.current_row += 1
                break
            elif direction.lower().strip() == "a" and self.current_col != 0:
                self.current_col -= 1
                break
            elif direction.lower().strip() == "d" and self.current_col != 8:
                self.current_col += 1
                break
            else:
                print("Invalid action")

    def fake_server_connection(self):
        print(f"Connecting to server {random.randint(10000, 99999)}...")
        self.show_loading()
        self.print_fake_logs(self.server_connect_logs_BefS)
        self.show_loading("Connecting To Server...")
        self.print_fake_logs(self.server_connect_logs_AftS)
        self.clear_screen()
        print(f"{Bcolors.OKGREEN}##################################{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}#       Copyright ClosedAI       #{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}#      NO UNAUTHORIZED ACCESS    #{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.OKGREEN}##################################{Bcolors.ENDC}")

    def play_decryption(self):
        # decryption_q_index = random.randint(0, len(self.python_questions) - 1)
        # decryption_q = self.python_questions[decryption_q_index]
        # decryption_ans = self.python_questions_ans[decryption_q_index]
        # self.fake_server_connection()
        # time.sleep(2)
        # input(
        #     f"{Bcolors.WARNING}{Bcolors.BOLD}>>Server: Press enter to start password recovery{Bcolors.ENDC}{Bcolors.ENDC}")
        # self.typewriter_print("Password recovery initiated...", color="bright_red", bolded=True)
        # self.typewriter_print(f"Enter previous server password: (hint, it's python code) {decryption_q}", color="bright_yellow")
        # user_ans = self.input_handler.handle_string_input("Insert password (python code) below")
        # if user_ans.replace("'", '"') == decryption_ans or user_ans.replace('"', "'") == decryption_ans:
        #     self.typewriter_print("Password recovery successful!", color="bright_green", bolded=True)
        #     time.sleep(2)
        #     return True
        # else:
        #     self.typewriter_print("Password recovery failed! Disconnecting from threat!", color="bright_red", bolded=True)
        #     time.sleep(2)
        #     return False
        # <-------Testing Code------->
        return True

    def play_intrusion(self):
        # intrusion_q_index = random.randint(0, len(self.number_riddles) - 1)
        # intrusion_q = self.number_riddles[intrusion_q_index]
        # intrusion_ans = self.number_riddles_ans[intrusion_q_index]
        # self.fake_server_connection()
        # time.sleep(2)
        # input(
        #     f"{Bcolors.WARNING}{Bcolors.BOLD}>>Server: Press enter to authenticate{Bcolors.ENDC}{Bcolors.ENDC}")
        # self.typewriter_print(f"{intrusion_q}", color="bright_yellow")
        # user_ans = self.input_handler.handle_int_input("Insert integer 2-factor authentication below")
        # if user_ans == intrusion_ans:
        #     self.typewriter_print("Access Granted!", color="bright_green", bolded=True)
        #     time.sleep(2)
        #     return True
        # else:
        #     self.typewriter_print("Failed to verify identity!", color="bright_red",
        #                           bolded=True)
        #     time.sleep(2)
        #     return False
        # <-------Testing Code------->
        return True

    def play_sys_manip(self):
        # self.fake_server_connection()
        # time.sleep(1)
        # input(
        #     f"{Bcolors.WARNING}{Bcolors.BOLD}>>Server: Press Enter to Debug Binary for (misplaced #2) Errors{Bcolors.ENDC}{Bcolors.ENDC}")
        # self.typewriter_print("Binary Debugging initiated...", color="bright_red", bolded=True)
        # self.typewriter_print("Regenerate binary map? (This will reset the binary map)", color="bright_yellow")
        # user_ans = self.input_handler.handle_bool_input()
        # if user_ans:
        #     return self.play_ericsweeper(new_board=True)
        # else:
        #     return self.play_ericsweeper()
        # <-------Testing Code------->
        return True
    def play_terminal(self):
        self.fake_server_connection()
        time.sleep(1)
        input(
            f"{Bcolors.WARNING}{Bcolors.BOLD}>>Server: Press Enter to Log In{Bcolors.ENDC}{Bcolors.ENDC}")
        self.typewriter_print("Logging in...", color="bright_red", bolded=True)
        self.show_loading()
        str_key = str(self.decryption_key)
        self.typewriter_print(f"The {self.current_floor + 1}th digit of the decryption key is {str_key[self.current_floor]}")
        time.sleep(2)
        return True

    def play_portal(self):
        self.fake_server_connection()
        print(f"{Bcolors.FAIL}##################################{Bcolors.ENDC}")
        print(f"{Bcolors.FAIL}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.FAIL}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.FAIL}#       ClosedAI Decryption      #{Bcolors.ENDC}")
        print(f"{Bcolors.FAIL}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.FAIL}#      NO UNAUTHORIZED ACCESS    #{Bcolors.ENDC}")
        print(f"{Bcolors.FAIL}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.FAIL}#                                #{Bcolors.ENDC}")
        print(f"{Bcolors.FAIL}##################################{Bcolors.ENDC}")
        time.sleep(2)
        self.typewriter_print("WARNING, you are trying to access the JPT model decryption portal", color="bright_red", bolded=True)
        time.sleep(2)
        self.typewriter_print("This portal is heavily guarded and will require the full decryption key to access", color="bright_red", bolded=True)
        time.sleep(2)
        self.typewriter_print("You have ONE try to enter the full decryption key", color="bright_red", bolded=True)
        time.sleep(2)
        print(f"{Bcolors.WARNING}{Bcolors.BOLD}>>ClosedAI_MasterServer: What is the decryption key?{Bcolors.ENDC}{Bcolors.ENDC}")
        user_ans = self.input_handler.handle_int_input("Insert decryption key below")
        if user_ans == self.decryption_key:
            self.typewriter_print("Access Granted!", color="bright_green", bolded=True)
            time.sleep(2)
            return True
        else:
            self.typewriter_print("Failed to verify identity!", color="bright_red",
                                  bolded=True)
            time.sleep(2)
            return False

    def play_floor(self, floor_num):
        floor_death = False
        floor_won = False
        self.current_floor = floor_num
        self.clear_screen()
        self.decryption_tasks_left = 3
        self.intrusion_tasks_left = 3
        self.sys_manipulation_tasks_left = 3
        while floor_won is False:
            print(
                f"{Bcolors.WARNING}{Bcolors.BOLD}<--------Connected to datacenter 0{self.current_floor + 1} :: Server[row:{self.current_row + 1}, col:{self.current_col + 1}] ::{self.server_ips[self.current_floor - 1]}--------->{Bcolors.ENDC}{Bcolors.ENDC}")
            for i in range(len(self.server_floors[self.current_floor])):
                for j in range(len(self.server_floors[self.current_floor][i])):
                    if i == self.current_row and j == self.current_col:
                        print(f"{Bcolors.OKGREEN}P{Bcolors.ENDC}", end=" ")
                    # elif self.server_floors[self.current_floor][i][j] != 0:
                    #     print(f"{Bcolors.FAIL}█{Bcolors.ENDC}", end=" ")
                    else:
                        print(self.server_floors[self.current_floor][i][j], end=" ")
                print()
            print()
            time.sleep(0.8)
            move_state = self.hack_menu()
            time.sleep(0.8)
            if move_state == "Terminated":
                floor_death = True
            elif move_state == "Floor Completed":
                floor_won = True
            elif move_state == "Game Won":
                floor_won = True
            elif move_state == "Portal Fail":
                floor_death = True
            input(f"{Bcolors.WARNING}{Bcolors.BOLD}Press enter to continue...{Bcolors.ENDC}{Bcolors.ENDC}")
            relative_positions = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1)
            ]

            for dx, dy in relative_positions:
                nx, ny = self.current_row + dx, self.current_col + dy
                if 0 <= nx < self.server_floors[self.current_floor].shape[0] and 0 <= ny < \
                        self.server_floors[self.current_floor].shape[1] and self.server_floors[self.current_floor][
                    nx, ny] == 4:
                    self.clear_screen()
                    print(f"{Bcolors.WARNING}AN ANTIVIRUS PROGRAM IS NEARBY, WATCH OUT!{Bcolors.ENDC}")
                    time.sleep(0.8)
                    input(f"{Bcolors.WARNING}{Bcolors.BOLD}Press enter to continue...{Bcolors.ENDC}{Bcolors.ENDC}")
                    break

            self.move_player()
            time.sleep(0.3)
            self.clear_screen()
        return floor_death

    def introduce_game(self):
        self.clear_screen()
        self.typewriter_print("Skip intro?")
        self.skip_intro = self.input_handler.handle_bool_input()
        if self.skip_intro is False:
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
                self.typewriter_print("The key is a 3 digit number.", color="bright_yellow", bolded=True)
                time.sleep(2)
                if self.quiz_rules_int("How many digits is the encryption key to hack ClosedAI?", 3):
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
        else:
            self.setup_game()

    def set_current_conditions(self):
        self.on_corrupt = False
        self.on_security = False
        self.on_empty = False
        self.on_decryption = False
        self.on_intrusion = False
        self.on_sys_manipulation = False
        self.on_terminal = False
        self.on_portal = False

        if self.server_floors[self.current_floor][self.current_row][self.current_col] == -1:
            self.on_corrupt = True
        elif self.server_floors[self.current_floor][self.current_row][self.current_col] == 0:
            self.on_empty = True
        elif self.server_floors[self.current_floor][self.current_row][self.current_col] == 1:
            self.on_decryption = True
        elif self.server_floors[self.current_floor][self.current_row][self.current_col] == 2:
            self.on_intrusion = True
        elif self.server_floors[self.current_floor][self.current_row][self.current_col] == 3:
            self.on_sys_manipulation = True
        elif self.server_floors[self.current_floor][self.current_row][self.current_col] == 4:
            self.on_security = True
            self.server_floors[self.current_floor][self.current_row][self.current_col] = 0
        elif self.server_floors[self.current_floor][self.current_row][self.current_col] == 5:
            self.on_terminal = True
        elif self.server_floors[self.current_floor][self.current_row][self.current_col] == 6:
            self.on_portal = True

    def generate_floor(self, with_security=False, with_portal=False):
        '''
        -1 = get a skill/move up down, 0 = empty, 1 = decryption, 2 = intrusion, 3 = manipulation, 4 antivirus,
        5 = terminal (give digit when all auth tasks complete), 6 firewall portal (fifth floor only)
        '''
        floor_grid = np.zeros((9, 9), dtype=int)
        # gen_vals = [1, 2, 3]
        # for val in gen_vals:
        #     count = 0
        #     while count < 3:
        #         rand_row = random.randint(0, 8)
        #         rand_col = random.randint(0, 8)
        #         if floor_grid[rand_row][rand_col] == 0:
        #             floor_grid[rand_row][rand_col] = val
        #             count += 1
        # skill_add_count = 0
        # while skill_add_count < 6:
        #     rand_row = random.randint(0, 8)
        #     rand_col = random.randint(0, 8)
        #     if floor_grid[rand_row][rand_col] == 0:
        #         floor_grid[rand_row][rand_col] = -1
        #         skill_add_count += 1
        # if with_security:
        #     security_count = 0
        #     while security_count < 5:
        #         rand_row = random.randint(0, 8)
        #         rand_col = random.randint(0, 8)
        #         if floor_grid[rand_row][rand_col] == 0:
        #             floor_grid[rand_row][rand_col] = 4
        #             security_count += 1
        # if with_portal:
        #     portal_count = 0
        #     while portal_count < 1:
        #         rand_row = random.randint(0, 8)
        #         rand_col = random.randint(0, 8)
        #         if floor_grid[rand_row][rand_col] == 0:
        #             floor_grid[rand_row][rand_col] = 6
        #             portal_count += 1
        # else:
        #     terminal_count = 0
        #     while terminal_count < 1:
        #         rand_row = random.randint(0, 8)
        #         rand_col = random.randint(0, 8)
        #         if floor_grid[rand_row][rand_col] == 0:
        #             floor_grid[rand_row][rand_col] = 5
        #             terminal_count += 1

        # <--------TESTING CODE---------->
        # for i in range(len(floor_grid)):
        #     for j in range(len(floor_grid[i])):
        #         print(floor_grid[i][j], end=" ")
        #     print()
        # floor_grid[1][1] = 4
        # floor_grid[0][0] = 3
        floor_grid[0][0] = 1
        floor_grid[0][1] = 1
        floor_grid[0][2] = 1
        floor_grid[0][3] = 2
        floor_grid[0][4] = 2
        floor_grid[0][5] = 2
        floor_grid[0][6] = 3
        floor_grid[0][7] = 3
        floor_grid[0][8] = 3
        floor_grid[1][0] = -1
        floor_grid[1][1] = -1
        floor_grid[1][2] = -1
        # floor_grid[1][3] = 4
        # floor_grid[1][4] = 4
        floor_grid[1][5] = 5
        if with_portal:
            floor_grid[1][6] = 6
        return floor_grid

    # <--------Modified Ericsweeper (Binary Debug in this game)---------->
    def play_ericsweeper(self, new_board=False):
        self.clear_screen()
        if new_board:
            self.sweep_board = np.zeros((10, 10), int)
            for i in range(len(self.sweep_board)):
                for j in range(len(self.sweep_board[i])):
                    self.sweep_board[i][j] = random.randint(0, 1)
            rand_row = random.randint(0, 9)
            rand_col = random.randint(0, 9)
            self.sweep_board[rand_row][rand_col] = 2
        sweep_board = self.sweep_board

        pos_x = random.randint(0, len(sweep_board[1]) - 1)
        pos_y = random.randint(0, len(sweep_board) - 1)

        # if you are started under a bomb you get moved to somewhere with no bomb under
        while sweep_board[pos_y][pos_x] == 2:
            for i in range(len(sweep_board)):
                for j in range(len(sweep_board[i])):
                    pos_x = j
                    pos_y = i
        previous_x = pos_x
        previous_y = pos_y
        immunity = 0
        counter = 0
        while counter < 25:
            self.clear_screen()
            print("<01001000 01100101 01111001 00100000 01001101 01110011 00101110>")
            print("<00100000 01001000 01100101 01100001 01101100 01100101 01111001>")
            print("Debug the binary by finding error 2's in the board!")
            print("You have " + str(25 - counter) + " tries left")
            for i in range(len(sweep_board)):
                for j in range(len(sweep_board[i])):
                    if i == pos_y and j == pos_x:
                        print(sweep_board[i][j], end=" ")
                    else:
                        print("█", end=" ")
                print()
            if sweep_board[pos_y][pos_x] == 0 or pos_y == previous_y and pos_x == previous_x or sweep_board[pos_y][pos_x] == 1:
                print("Binary: Normal")
            else:
                print(f"{Bcolors.FAIL}Binary: Error Found{Bcolors.ENDC}")
                time.sleep(0.3)
                print(f"{Bcolors.FAIL}Vulnerability Found!{Bcolors.ENDC}")
                time.sleep(1)
                return True
            previous_x = pos_x
            previous_y = pos_y
            direction = input("w. up, s. down, d. right, a. left\n>>>")
            if direction == 'w':
                if pos_y == 0:
                    print("Can't move up anymore! choose another direction")
                else:
                    pos_y -= 1
            elif direction == 's':
                if pos_y == 9:
                    print("Can't move down anymore! choose another direction")
                else:
                    pos_y += 1
            elif direction == 'd':
                if pos_x == 9:
                    print("Can't move right anymore! choose another direction")
                else:
                    pos_x += 1
            elif direction == 'a':
                if pos_x == 0:
                    print("Can't move left anymore! choose another direction")
                else:
                    pos_x -= 1
            else:
                print("Oops! That's not an option!")
            counter += 1
        return False


if __name__ == "__main__":
    # using different clears so this works on more platforms
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Pen & Paper is recommended for this game")
    while True:
        try:
            name = input("Enter your name!\n>>>")
            break
        except ValueError and TypeError:
            print("Invalid input, try again.")

    player = HackerPlayer(name)
    game_master = GameMaster(player)
    time.sleep(0.5)
    game_master.introduce_game()

    # <------testing code(DO NOT RUN)------------>
    # test_player = HackerPlayer("Eric")
    # test_game_master = GameMaster(test_player)
    # test_game_master.play_portal()
