"""
Eric
October 9th, 2023

Sources:
Referenced previously written code for the adventure game--did not copy however since this is a little bit different
PyGame Video player - https://github.com/ree1261/pyvidplayer2
Got the colors for minesweeper numbers from here - https://www.reddit.com/r/BattleForDreamIsland/comments/gcbwv7/did_you_know_that_4_2_and_other_numbers_from_x/
Referenced pygame "Named Colors" for color strings - https://www.pygame.org/docs/ref/color_list.html
Tutorial on PyGame buttons because somehow this game library does not have buttons - https://youtu.be/G8MYGDf_9ho?si=1QJOf3QUy1jC4BXb

*THIS VERSION HAS THE EZINPUT & DEVTOOLS LIBRARY IN THE SAME SCRIPT*
*please do all pip installs before running*
*BREW INSTALL FFMPEG & Portaudio before running*

Reflection:
This second checkpoint includes the conversion of the game from a text-based game to a GUI game. I used PyGame,
a library that I have experience with to create the GUI game. I think this is a good way to scale the difficulty of the project
to my skill level, and it also provides a better user experience than a text-based game. I also added a video intro to the game
to make it more interesting. I made the intro in After Effects. I also added a "first move" feature that makes it so that the
first click will never be on a mine. Overall, this was a really nice refresher on coding with 2D arrays and pygame.

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
from collections import deque


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
        self.rows = 10
        self.cols = 10
        self.number_color_map = {
            1: "blue",
            2: "darkgreen",
            3: "red",
            4: "blue4",
            5: "maroon",
            6: "paleturquoise4",
            7: "black",
            8: "indianred1"
        }
        self.cell_color = "grey30"
        self.revealed_cell_color = "grey"
        self.marked_cell_color = "red"
        self.width = 1000
        self.height = 800
        self.map_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", int(self.height / self.rows) - 20)
        self.info_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", 20)
        self.game_won = False
        self.game_lost = False
        self.num_on_mines = 0
        self.flags = 0
        self.mines = 0

    def generate_map(self, width, height, num_mines):
        self.rows = width
        self.cols = height
        self.flags = num_mines
        self.mines = num_mines
        if int(self.height / self.rows) - 50 < 0:
            self.map_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", 30)
        else:
            self.map_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", int(self.height / self.rows) - 20)
        # generate a 2d array that has gutters with zeros
        generated_map = np.zeros((width + 2, height + 2))
        # pick random position within the gutter boundaries n times and set it to -1
        for num in range(num_mines):
            random_row = random.randint(1, width)
            random_col = random.randint(1, height)
            while generated_map[random_col][random_row] == -1:
                random_row = random.randint(1, width)
                random_col = random.randint(1, height)
            print(f"Mine placed at ({random_row}, {random_col})")
            generated_map[random_col][random_row] = -1
            # look around the mine and add 1 to the number of mines around, don't do anything if it's a mine
            for dx, dy in self.relative_positions:
                nx, ny = random_row + dx, random_col + dy
                if generated_map[ny][nx] != -1:
                    generated_map[ny][nx] += 1
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
            if self.solution_map[nx][ny] != -1 and self.solution_map[nx][ny] != -2:
                self.solution_map[nx][ny] -= 1
        random_row = random.randint(1, self.rows)
        random_col = random.randint(1, self.cols)
        while self.solution_map[random_row][random_col] == -1 or self.solution_map[random_row][random_col] == -2:
            random_row = random.randint(1, self.rows)
            random_col = random.randint(1, self.cols)
        new_mines_around = 0
        for dx, dy in self.relative_positions:
            nx, ny = row + dx, col + dy
            print(f"({nx}, {ny})")
            if self.solution_map[ny][nx] == -1:
                new_mines_around += 1
                print("added one")
        self.solution_map[row][col] = new_mines_around
        # look around the mine and add 1 to the number of mines around, don't do anything if it's a mine
        for dx, dy in self.relative_positions:
            nx, ny = random_row + dx, random_col + dy
            if self.solution_map[nx][ny] != -1 and self.solution_map[nx][ny] != -2:
                self.solution_map[nx][ny] += 1
        self.solution_map[random_row][random_col] = -1
        print(f"Moved mine from ({col}, {row}) to ({random_col}, {random_row})")
        if self.cover_map[random_row][random_col] == 2:
            self.check_cover(random_row, random_col)

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
        icon = pygame.image.load("Ericsweeper_thumb.png")
        pygame.display.set_icon(icon)
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
                    sys.exit()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            clock.tick(60)

    def dfs(self, graph, start):
        # implement dfs to start for all 0 around it
        # create a stack
        stack = deque()
        # push the start node
        stack.append(start)
        # create a set to store visited nodes
        visited = set()
        # while the stack is not empty
        while stack:
            # pop a node from the stack
            node = stack.pop()
            # if the node is not visited
            if node not in visited:
                # mark it as visited
                visited.add(node)
                for neighbour in graph[node]:
                    stack.append(neighbour)
        return visited

    def draw_mine(self, screen, solution_board, cover_board):
        cell_size = self.height / self.rows
        screen.fill(self.BGCOLOR)
        for i, col in enumerate(solution_board):
            if i == 0 or i == len(solution_board) - 1:
                continue
            y = (i - 1) * cell_size
            for j, cell in enumerate(col):
                if j == 0 or j == len(col) - 1:
                    continue
                x = (j - 1) * cell_size + ((1000 - cell_size * self.cols) / 2)
                covered = cover_board[i][j]
                if covered == 0:
                    pygame.draw.rect(screen, self.cell_color, (x, y, cell_size, cell_size), border_radius=30)
                    pygame.draw.rect(screen, "white", (x, y, cell_size, cell_size), width=3, border_radius=30)
                    pygame.draw.rect(screen, "black", (x, y, cell_size, cell_size), 1)
                    continue
                elif covered == 1:
                    pygame.draw.rect(screen, self.revealed_cell_color, (x, y, cell_size, cell_size), border_radius=30)
                    pygame.draw.rect(screen, "white", (x, y, cell_size, cell_size), width=3, border_radius=30)
                    pygame.draw.rect(screen, "black", (x, y, cell_size, cell_size), 1)
                elif covered == 2:
                    pygame.draw.rect(screen, self.marked_cell_color, (x, y, cell_size, cell_size), border_radius=30)
                    pygame.draw.rect(screen, "white", (x, y, cell_size, cell_size), width=3, border_radius=30)
                    pygame.draw.rect(screen, "black", (x, y, cell_size, cell_size), 1)
                    continue
                if cell > 0:
                    text = self.map_font.render(str(cell), 1, self.number_color_map[cell])
                    screen.blit(text, (
                    x + (cell_size / 2 - text.get_width() / 2), y + (cell_size / 2 - text.get_height() / 2)))
                # ONLY ENABLE THIS IF YOU WANT TO SEE THE SOLUTION MAP
                elif cell == -1:
                    text = self.map_font.render(str(cell), 1, "black")
                    screen.blit(text, (
                    x + (cell_size / 2 - text.get_width() / 2), y + (cell_size / 2 - text.get_height() / 2)))
        screen.blit(self.info_font.render("Flags:", 1, "white"), (10, 30))
        if self.flags > 6:
            screen.blit(self.info_font.render(str(self.flags), 1, "green"), (10, 50))
        elif self.flags > 3:
            screen.blit(self.info_font.render(str(self.flags), 1, "yellow"), (10, 50))
        else:
            screen.blit(self.info_font.render(str(self.flags), 1, "red"), (10, 50))

        pygame.display.update()

    def check_cover(self, row, col):
        # check if the cell is a mine
        if self.solution_map[row][col] == -1 and self.cover_map[row][col] == 2:
            # if it is a mine, and you just marked it
            self.num_on_mines += 1
        elif self.solution_map[row][col] == -1 and self.cover_map[row][col] == 0 and self.flags > 0:
            # if it is a mine, but you just un marked it
            self.num_on_mines -= 1


    def play_game(self):
        # pygame setup
        pygame.init()
        screen = pygame.display.set_mode((1000, 800))
        clock = pygame.time.Clock()
        running = True
        icon = pygame.image.load("Ericsweeper_thumb.png")
        pygame.display.set_icon(icon)
        first_move = True

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_row, click_col = self.get_calibrated_click_position(pygame.mouse.get_pos())
                    # print(click_col)
                    if event.button == 1:
                        # debugging position calibration
                        # print(click_row, click_col)
                        if click_row >= self.rows or click_col >= self.cols:
                            continue
                        if first_move:
                            if self.solution_map[click_col + 1][click_row + 1] == -1:
                                self.first_move_map_update(click_col + 1, click_row + 1)
                            first_move = False
                        if self.cover_map[click_col + 1][click_row + 1] == 2:
                            self.flags += 1
                        self.cover_map[click_col + 1][click_row + 1] = 1
                        if self.solution_map[click_col + 1][click_row + 1] == -1:
                            self.game_lost = True

                    elif event.button == 3:
                        # debugging position calibration
                        # print(click_row, click_col)
                        if click_row >= self.rows or click_col >= self.cols or self.cover_map[click_col + 1][
                            click_row + 1] == 1:
                            continue
                        if self.cover_map[click_col + 1][click_row + 1] == 2:
                            self.cover_map[click_col + 1][click_row + 1] = 0
                            if not first_move:
                                self.check_cover(click_col + 1, click_row + 1)
                            self.flags += 1
                        elif self.flags > 0:
                            self.cover_map[click_col + 1][click_row + 1] = 2
                            if not first_move:
                                self.check_cover(click_col + 1, click_row + 1)
                            self.flags -= 1
                        elif self.flags == 0:
                            continue



            # self.print_map()
            self.draw_mine(screen, self.solution_map, self.cover_map)
            print(f"{self.num_on_mines}, {self.mines}")
            if self.num_on_mines == self.mines:
                self.game_won = True
                for i in range(1, len(self.cover_map)-1):
                    for j in range(1, len(self.cover_map[i])-1):
                        visibility = int(self.cover_map[i][j])
                        print(visibility)
                        if visibility == 0:
                            self.game_won = False

            if self.game_won:
                self.play_endscreen(True)
            elif self.game_lost:
                self.play_endscreen(False)
            # flip() the display to put work on screen
            # pygame.display.flip()
            # clock.tick(60)
        pygame.quit()

    def play_endscreen(self, win):
        icon = pygame.image.load("Ericsweeper_thumb.png")
        pygame.display.set_icon(icon)
        screen = pygame.display.set_mode((1000, 800))
        win_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", 55)
        while True:
            if win:
                text = win_font.render("You won!", 1, "white")
            else:
                text = win_font.render("You lost!", 1, "white")
            screen.blit(text, (500 - text.get_width() / 2, 400 - text.get_height() / 2))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


    def get_calibrated_click_position(self, click_position):
        click_x, click_y = click_position
        cell_size = self.height / self.rows
        row = click_x / cell_size - ((1000 - cell_size * self.cols) / 2) / cell_size
        col = click_y / cell_size

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
            # impossible boxes, no bombs, either many bombs, etc
            if int(user_argument[1]) < 2 or int(user_argument[2]) < 2 or int(user_argument[3]) < 1 or int(
                    user_argument[3]) >= int(user_argument[1]) * int(user_argument[2]):
                print("Invalid input, please try again.")
            elif abs(int(user_argument[1]) - int(user_argument[2])) >= 3 or int(user_argument[1]) > 21 or int(
                    user_argument[2]) > 21:
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
