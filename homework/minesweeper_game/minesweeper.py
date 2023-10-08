"""
Eric
October 6th, 2023

Sources:
Referenced previously written code for the adventure game--did not copy however since this is a little bit different
PyGame Video player - https://github.com/ree1261/pyvidplayer2
*THIS VERSION HAS THE EZINPUT & DEVTOOLS LIBRARY IN THE SAME SCRIPT*
*please do all pip installs before running*
*BREW INSTALL FFMPEG & Portaudio before running*

Reflection:


Have a good day! :)

On my honor, I have neither given nor received unauthorized aid on this assignment.
"""

import numpy as np
import sys
import os
import random
import time
import pygame
from pyvidplayer2 import Video
import matplotlib.pyplot as plt


# <--------------------------- Self Written Packages --------------------------->
class MinesweeperDevTools:
    def __init__(self):
        self.version = "0.0.1"
        self.author = "Eric Yang'25"

    def view_map_matplotlib(self, map):
        plt.imshow(map, cmap="CMRmap")
        plt.show()


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


def clear_screen():
    '''
    clears terminal screen with multi-os support
    :return: nothing
    '''
    # Using os.system to clear the terminal screen, short if else to support multiple OS
    os.system('cls' if os.name == 'nt' else 'clear')


class MinesweeperGM:
    def __init__(self):
        # store map and "look around" positions
        self.solution_map = None
        self.relative_positions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        self.cover_map = None
        self.BGCOLOR = (19, 19, 19)
        self.rows = 0
        self.cols = 0
        self.map_font = pygame.font.SysFont("Arial", 20)

    def generate_map(self, width, height, num_mines):
        self.rows = width
        self.cols = height
        # generate a 2d array that has gutters with zeros
        generated_map = np.zeros((width + 2, height + 2))
        # pick random position within the gutter boundaries n times and set it to -1
        for num in range(num_mines):
            random_row = random.randint(1, width)
            random_col = random.randint(1, height)
            generated_map[random_row][random_col] = -1
            # look around the mine and add 1 to the number of mines around, don't do anything if it's a mine
            for dx, dy in self.relative_positions:
                nx, ny = random_row + dx, random_col + dy
                if generated_map[nx][ny] != -1:
                    generated_map[nx, ny] += 1
        # set the gutter to -2
        for row_count in range(len(generated_map)):
            for col_count in range(len(generated_map[row_count])):
                if row_count == 0 or row_count == len(generated_map) - 1:
                    generated_map[row_count][col_count] = -2
                if col_count == 0 or col_count == len(generated_map[row_count]) - 1:
                    generated_map[row_count][col_count] = -2
        # set the map to the generated map, dtype int because numpy comes with float by default
        self.solution_map = np.array(generated_map, dtype=int)
        self.cover_map = np.zeros((width + 2, height + 2))

    def print_map(self):
        for i in range(1, len(self.solution_map) - 1):
            for j in range(1, len(self.solution_map[i]) - 1):
                if self.solution_map[i][j] == -1:
                    print("M", end=" ")
                elif self.solution_map[i][j] == -2:
                    print("X", end=" ")
                else:
                    print(self.solution_map[i][j], end=" ")
            print()


    def play_intro(self):
        clock = pygame.time.Clock()
        vid = Video("esweepintro.mp4")
        screen = pygame.display.set_mode((1000, 800))
        while True:
            vid.draw(screen, (0, 0), force_draw=False)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    vid.close()
                    self.play_game()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()
            clock.tick(60)

    def draw_mine(self, screen, solution_board, cover_board):
        cell_size = self.cols // self.rows
        screen.fill(self.BGCOLOR)
        pygame.display.update()

    def play_game(self):
        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((1000, 800))
        clock = pygame.time.Clock()
        running = True

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill(self.BGCOLOR)
            pygame.display.update()
            # flip() the display to put your work on screen
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()



if __name__ == "__main__":

    # <--------------------------- Production Section --------------------------->
    user_argument = sys.argv
    while True:
        # input argument error handling
        # no arguments
        if len(user_argument) < 4:
            print("Invalid input, please try again.")
        # if there are arguments, then...
        else:
            # impossible boxes, no bombs, too many bombs, etc
            if int(user_argument[1]) < 2 or int(user_argument[2]) < 2 or int(user_argument[3]) < 1 or int(user_argument[3]) > int(user_argument[1]) * int(user_argument[2]):
                print("Invalid input, please try again.")
            # if there are no errors, then break the loop
            else:
                user_width = int(user_argument[1])
                user_height = int(user_argument[2])
                user_num_mines = int(user_argument[3])
                break
        # if there are no arguments, then ask for input again
        if len(user_argument) < 4:
            user_argument.append(EZInputHandlerBase().handle_int_input("Please enter the width of the map."))
            user_argument.append(EZInputHandlerBase().handle_int_input("Please enter the height of the map."))
            user_argument.append(EZInputHandlerBase().handle_int_input("Please enter the number of mines."))
        # if there are arguments, but they are incorrect, then ask for input again
        else:
            user_argument[1] = EZInputHandlerBase().handle_int_input("Please enter the width of the map.")
            user_argument[2] = EZInputHandlerBase().handle_int_input("Please enter the height of the map.")
            user_argument[3] = EZInputHandlerBase().handle_int_input("Please enter the number of mines.")
        clear_screen()

    # just getting our object going
    minesweeper_controller = MinesweeperGM()
    minesweeper_controller.generate_map(user_width, user_height, user_num_mines)

    # <--------------------------- Development Section + Dev Package --------------------------->

    # ENABLE THESE IMPORTS ONLY WHEN DEVELOPING
    #
    # dev_tools = MinesweeperDevTools()
    #
    # # Show the image
    # dev_tools.view_map_matplotlib(minesweeper_controller.map)
    #
    # # Print the map
    # minesweeper_controller.print_map()
    minesweeper_controller.play_intro()
