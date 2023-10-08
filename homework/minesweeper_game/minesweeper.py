"""
Eric
October 6th, 2023

Sources:
Referenced previously written code for the adventure game--did not copy however since this is a little bit different
PyGame Video player - https://github.com/ree1261/pyvidplayer2
Got the colors for minesweeper numbers from here - https://www.reddit.com/r/BattleForDreamIsland/comments/gcbwv7/did_you_know_that_4_2_and_other_numbers_from_x/
Referenced pygame "Named Colors" for color strings - https://www.pygame.org/docs/ref/color_list.html


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
        self.map_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", 35)
        self.number_color_map = {
            1: "blue",
            2: "green",
            3: "red",
            4: "purple",
            5: "maroon",
            6: "turquoise",
            7: "black",
            8: "gray"
        }
        self.cell_color = "grey"
        self.revealed_cell_color = "grey22"
        self.width = 1000
        self.height = 800

    def generate_map(self, width, height, num_mines):
        self.rows = width
        self.cols = height
        # generate a 2d array that has gutters with zeros
        generated_map = np.zeros((width + 2, height + 2))
        # pick random position within the gutter boundaries n times and set it to -1
        for num in range(num_mines):
            random_row = random.randint(1, width)
            random_col = random.randint(1, height)
            while random_row == -1 and random_col == -1:
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

    def first_move_map_update(self, row, col):
        """
        If the first move is a mine, then move the mine to a random location and update the map
        :param row: row of old mine
        :param col: col of old mine
        :return: Nothing, updates self.solution_map with a new mine position
        """
        self.solution_map[row][col] = 0
        for dx, dy in self.relative_positions:
            nx, ny = row + dx, col + dy
            if self.solution_map[nx][ny] != -1:
                self.solution_map[nx, ny] -= 1
        random_row = random.randint(1, self.rows)
        random_col = random.randint(1, self.cols)
        while random_row == -1 and random_col == -1:
            random_row = random.randint(1, self.rows)
            random_col = random.randint(1, self.cols)
        self.solution_map[random_row][random_col] = -1
        # look around the mine and add 1 to the number of mines around, don't do anything if it's a mine
        for dx, dy in self.relative_positions:
            nx, ny = random_row + dx, random_col + dy
            if self.solution_map[nx][ny] != -1:
                self.solution_map[nx, ny] += 1

    # this is basically never used past development, but it's here just in case
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
        cell_size = self.height / self.rows
        screen.fill(self.BGCOLOR)
        for i, row in enumerate(solution_board):
            if i == 0 or i == len(solution_board) - 1:
                continue
            y = (i - 1) * cell_size
            for j, cell in enumerate(row):
                if j == 0 or j == len(row) - 1:
                    continue
                x = (j - 1) * cell_size + ((1000 - cell_size * self.cols)/2)
                covered = cover_board[i][j]
                if covered == 0:
                    pygame.draw.rect(screen, self.cell_color, (x, y, cell_size, cell_size), border_radius=30)
                    pygame.draw.rect(screen, "white", (x, y, cell_size, cell_size), width=5, border_radius=30)
                    pygame.draw.rect(screen, "black", (x, y, cell_size, cell_size), 2)
                    continue
                elif covered == 1:
                    pygame.draw.rect(screen, self.revealed_cell_color, (x, y, cell_size, cell_size), border_radius=30)
                    pygame.draw.rect(screen, "white", (x, y, cell_size, cell_size), width=5, border_radius=30)
                    pygame.draw.rect(screen, "black", (x, y, cell_size, cell_size), 2)
                if cell > 0:
                    text = self.map_font.render(str(cell), 1, self.number_color_map[cell])
                    screen.blit(text, (x + (cell_size/2 - text.get_width()/2), y + (cell_size/2 - text.get_height()/2)))
                # ONLY ENABLE THIS IF YOU WANT TO SEE THE SOLUTION MAP
                # elif cell == -1:
                #     text = self.map_font.render(str(cell), 1, "black")
                #     screen.blit(text, (x + (cell_size / 2 - text.get_width() / 2), y + (cell_size / 2 - text.get_height() / 2)))

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_row, click_col = self.get_calibrated_click_position(pygame.mouse.get_pos())
                    # debugging position calibration
                    # print(click_row, click_col)

            self.draw_mine(screen, self.solution_map, self.cover_map)
            # # flip() the display to put your work on screen
            # pygame.display.flip()
            # clock.tick(60)
        pygame.quit()

    def get_calibrated_click_position(self, click_position):
        click_x, click_y = click_position
        cell_size = self.height / self.rows
        row = click_x // cell_size - ((1000 - cell_size * self.cols)/2) // cell_size
        col = click_y // cell_size

        return int(row), int(col)




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
            elif abs(int(user_argument[1]) - int(user_argument[2])) >= 3:
                print("Your grid is too long or too wide, please try again.")
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
