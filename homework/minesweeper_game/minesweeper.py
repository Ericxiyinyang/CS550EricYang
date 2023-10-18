"""
Eric
October 19th, 2023

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
I really, really liked this project. Although we started out with just a terminal interface and basic map generation, the final product is the
full, graphic, and interactive version of minesweeper that I wanted to see. I think that I scaled the difficulty of this project
relatively well to both review dealing with 2D arrays while also trying something new: making a pygame. As with any project
where a third-party library is used, I had to re-read pygame's docs to figure out how I can incorporate it with my existing
terminal code. Additionally, play testing played an important role in finding bugs I simply did not think of or didn't have
time to try. It's only because of how much play testing went into this game that it is as polished as it is now. One thing
I decided to focus on this time (since I didn't do quite a good job on it in the last project) was to really comment out my code.
In the last project, I only used docstrings to document each method, but this time I also added comments to the code itself.
The massive line count you see is primarily due to the comments I added. I think that this is a good habit to get into, and
I will continue to provide detailed documentation for my code in the future.

(The trickiest functions in the project are also documented in a video I made, it's in this folder!)

Have a good day! :)

On my honor, I have neither given nor received unauthorized aid on this assignment.
"""


"""
importing relevant packages: Numpy for map handeling, sys for command line arguments, os for clearing the screen,
random for random, time for time, pygame as the rendering engine pyvidplayer2 for the tutorial video, and deque for
faster DFS algorithm to handle cleaning zeros in larger maps (I was looking for something similar to priority_queue in C++. 
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
"""
Minesweeper devtools package that I used to visualize the map before implementing the pygame interface.
The terminal interface was just bad for visualizing the generation method and the map itself so I used
matplotlib to visualize the map.
"""
class MinesweeperDevTools:
    def __init__(self):
        self.version = "0.0.1"
        self.author = "Eric Yang'25"

    def view_map_matplotlib(self, map):
        # making basic matplotlib grid and mapping colors to the "CMRmap" color map
        plt.imshow(map, cmap="CMRmap")
        plt.show()

"""
The same old input handler that I've been using for the past few project, though very lightly used this
time around since I made a pygame.
"""
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

"""
The actual class that runs the whole show, it houses the different pygame scenes and also generation method
that we need to use. It also stores both the solution_map and the cover_map.
"""
class MinesweeperGM:
    """
    This class should be initialized with the number of rows, columns, and mines in order to generate a placeholder
    solution_map since we need to make sure the first click is never a mine.
    """
    def __init__(self, rows, cols, mines):
        # "look around" positions, so we can just use this instead of rewriting all the time
        self.relative_positions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        # Storing the colors & number colors in a dict to map it to the number
        self.BGCOLOR = (19, 19, 19)
        self.rows = rows
        self.cols = cols
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
        # pygame graphics setup (screen + fonts)
        self.width = 1000
        self.height = 800
        self.map_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", int(self.height / self.rows) - 20)
        self.info_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", 20)
        # game conditions
        self.game_won = False
        self.game_lost = False
        # variables that track the game
        self.num_on_mines = 0
        self.flags = 0
        self.mines = mines
        # initialize the maps with just zeros and gutters but the same size as the actually generated map
        self.solution_map = np.zeros((self.cols + 2, self.rows + 2))
        self.cover_map = np.zeros((self.cols + 2, self.rows + 2))

    def is_within_safe_zone(self, row, col, first_click_row, first_click_col, safe_radius):
        """Check if given (row, col) is within the safe zone around the user's first click."""
        """
        The idea: if |row - first_click_row| <= safe_radius and |col - first_click_col| <= safe_radius, then the cell is
        within the safe zone. This is because the safe zone is a square with side length (1 + (2*safe_radius))^2. If it
        is within this safe zone, then we return True, else we return False.
        """
        return abs(row - first_click_row) <= safe_radius and abs(col - first_click_col) <= safe_radius

    """
    This is one of the KEY methods of the GM class. It generates the map with respect to the first click that the player
    makes
    """
    def generate_map(self, width, height, num_mines, first_click_row, first_click_col, safe_radius):
        # First, we will calculate the size of the pygame font to be used to display the numbers based on map's height
        if int(self.height / self.rows) - 50 < 0:
            self.map_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", 30)
        else:
            self.map_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", int(self.height / self.rows) - 20)


        # generate a 2d array that has gutters with zeros
        generated_map = np.zeros((height + 2, width + 2))


        # pick random position within the gutter boundaries n times and set it to -1
        # loop through how many times we want to "place a mine"
        for num in range(num_mines):
            # first, get a random [][] index
            random_row = random.randint(1, width)
            random_col = random.randint(1, height)
            # however, if the index is already a bomb, or it is within a 2 block radius of the first click, find another
            while generated_map[random_col][random_row] == -1 or self.is_within_safe_zone(random_row, random_col, first_click_row, first_click_col, safe_radius):
                # the "finding another one" everytime we get a bad index
                random_row = random.randint(1, width)
                random_col = random.randint(1, height)
            # print(f"width: {width}, height: {height}")
            # used this for debugging mine placement
            # print(f"Mine placed at ({random_row}, {random_col})")
            # print(f"random_row: {random_row}, random_col: {random_col}")
            # set the "good" random index to -1
            generated_map[random_col][random_row] = -1


            # look around the mine and add 1 to the number of mines around, don't do anything if it's a mine
            # for each set of +-x & +-y loop through these changes
            for dx, dy in self.relative_positions:
                # calculate the new x and y using the index the bomb is at + the lookaround delta
                nx, ny = random_row + dx, random_col + dy
                # print(f"({nx}, {ny})")
                # if the new x and y is not a bomb, then add 1 to the number of mines around
                if generated_map[ny][nx] != -1:
                    generated_map[ny][nx] += 1
            # print("COMPLETE")

        # set the gutter to -2
        for row_count in range(len(generated_map)):
            for col_count in range(len(generated_map[row_count])):
                # check if the row or col is a gutter (end/beginning), if it is, set it to -2
                if row_count == 0 or row_count == len(generated_map) - 1:
                    generated_map[row_count][col_count] = -2
                if col_count == 0 or col_count == len(generated_map[row_count]) - 1:
                    generated_map[row_count][col_count] = -2


        # set the map to the generated map, dtype int because numpy comes with float by default
        self.solution_map = np.array(generated_map, dtype=int)
        self.cover_map = np.zeros((height + 2, width + 2), dtype=int)

    """
    This was how it used to account for the user's first move, by basically moving the mine to a random location
    if the user clicked on a mine. However, it does not work well for DFS and it only provides that the current space
    is empty, which sometimes leads to nothing else getting revealed.
    """
    # def first_move_map_update(self, row, col):
    #     """
    #     If the first move is a mine, then move the mine to a random location and update the map
    #     :param row: row of old mine
    #     :param col: col of old mine
    #     :return: Nothing, updates self.solution_map with a new mine position
    #     """
    #     self.solution_map[row][col] = 0
    #     for dx, dy in self.relative_positions:
    #         nx, ny = row + dx, col + dy
    #         if self.solution_map[nx][ny] != -1 and self.solution_map[nx][ny] != -2:
    #             self.solution_map[nx][ny] -= 1
    #     random_row = random.randint(1, self.rows)
    #     random_col = random.randint(1, self.cols)
    #     while self.solution_map[random_row][random_col] == -1 or self.solution_map[random_row][random_col] == -2:
    #         random_row = random.randint(1, self.rows)
    #         random_col = random.randint(1, self.cols)
    #     new_mines_around = 0
    #     for dx, dy in self.relative_positions:
    #         nx, ny = row + dx, col + dy
    #         print(f"({nx}, {ny})")
    #         if self.solution_map[ny][nx] == -1:
    #             new_mines_around += 1
    #             print("added one")
    #     self.solution_map[row][col] = new_mines_around
    #     # look around the mine and add 1 to the number of mines around, don't do anything if it's a mine
    #     for dx, dy in self.relative_positions:
    #         nx, ny = random_row + dx, random_col + dy
    #         if self.solution_map[nx][ny] != -1 and self.solution_map[nx][ny] != -2:
    #             self.solution_map[nx][ny] += 1
    #     self.solution_map[random_row][random_col] = -1
    #     print(f"Moved mine from ({col}, {row}) to ({random_col}, {random_row})")
    #     if self.cover_map[random_row][random_col] == 2:
    #         self.check_cover(random_row, random_col)



    # this is basically never used past development, but it's here just in case
    def print_map(self):
        # loop through entire 2d array without the gutter indicies
        for i in range(1, len(self.solution_map) - 1):
            for j in range(1, len(self.solution_map[i]) - 1):
                # if the thing at this index is a mine, print M. If it's a gutter, print X. Else, print the number
                if self.solution_map[i][j] == -1:
                    print("M", end=" ")
                elif self.solution_map[i][j] == -2:
                    print("X", end=" ")
                else:
                    print(self.solution_map[i][j], end=" ")
            print()

    """
    This method plays the introduction video by utilizing the pygame video player.
    """
    def play_intro(self):
        # load the pygame icon for this scene
        icon = pygame.image.load("Ericsweeper_thumb.png")
        # set the game icon with pygame.display
        pygame.display.set_icon(icon)
        # start a clock for the video just in case we need it
        clock = pygame.time.Clock()
        # initialize the video with the pyvidplayer2 library's Video() class, basically we made a new Video object
        vid = Video("esweepintro.mp4")
        # set screen ratios for this video
        screen = pygame.display.set_mode((1000, 800))

        # this while true represents every frame of the game
        while True:
            # draw the video frame by frame
            vid.draw(screen, (0, 0), force_draw=False)
            # update the display so every frame is drawn
            pygame.display.update()

            # record user_events throughout the whole session
            for event in pygame.event.get():
                # if the user clicks the mouse, close the video and start the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    vid.close()
                    self.play_game()
                    sys.exit()
                # if the user clicks the X, close the video and quit the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # tick the clock to make sure the video is playing at constant FPS
            clock.tick(60)

    """
    This function utilizes pygame to deliver a frame in the game, the main game loop will call this every frame to update
    the screen.
    """
    def draw_mine(self, screen, solution_board, cover_board):
        # a cell is a square, so it's l = available height pixels/rows
        if self.rows > self.cols:
            cell_size = (self.width - 200) / self.rows
        else:
            cell_size = self.height / self.cols
        # fill in the bg color
        screen.fill(self.BGCOLOR)
        # loop through the solution board
        for i, col in enumerate(solution_board):
            # skip the gutter indices
            if i == 0 or i == len(solution_board) - 1:
                continue
            # calculate the y position of the cell this is dependent on if the rows or cols are bigger
            if self.cols > self.rows:
                y = (i - 1) * cell_size
            else:
                y = (i - 1) * cell_size + ((800 - cell_size * self.cols) / 2)
            for j, cell in enumerate(col):
                # skip the gutter indices
                if j == 0 or j == len(col) - 1:
                    continue
                # calculate the x position of the cell, cell position - 1 b/c gutters * cell size. + 1000 - cell_size * self.cols)/2 b/c we want to center the board
                x = (j - 1) * cell_size + ((1000 - cell_size * self.rows) / 2)

                # get the cover information from the cover board
                covered = cover_board[i][j]

                # draw the cell based on the cover information
                if covered == 0:
                    # if the cell is covered, draw the cell color, then draw a white border, then draw a black border
                    pygame.draw.rect(screen, self.cell_color, (x, y, cell_size, cell_size), border_radius=int(30 * cell_size/80))
                    pygame.draw.rect(screen, "white", (x, y, cell_size, cell_size), width=3, border_radius=int(30 * cell_size/80))
                    pygame.draw.rect(screen, "black", (x, y, cell_size, cell_size), 1)
                    continue
                elif covered == 1:
                    # if the cell is revealed, draw the revealed cell color, then draw a white border, then draw a black border
                    pygame.draw.rect(screen, self.revealed_cell_color, (x, y, cell_size, cell_size), border_radius=int(30 * cell_size/80))
                    pygame.draw.rect(screen, "white", (x, y, cell_size, cell_size), width=3, border_radius=int(30 * cell_size/80))
                    pygame.draw.rect(screen, "black", (x, y, cell_size, cell_size), 1)
                elif covered == 2:
                    # if the cell is marked, draw the marked cell color, then draw a white border, then draw a black border
                    pygame.draw.rect(screen, self.marked_cell_color, (x, y, cell_size, cell_size), border_radius=int(30 * cell_size/80))
                    pygame.draw.rect(screen, "white", (x, y, cell_size, cell_size), width=3, border_radius=int(30 * cell_size/80))
                    pygame.draw.rect(screen, "black", (x, y, cell_size, cell_size), 1)
                    continue
                if cell > 0:
                    # if the cell is a number, draw the number in the color that corresponds to the number
                    text = self.map_font.render(str(cell), 1, self.number_color_map[cell])
                    screen.blit(text, (
                    x + (cell_size / 2 - text.get_width() / 2), y + (cell_size / 2 - text.get_height() / 2)))
                # ONLY ENABLE THIS IF YOU WANT TO SEE THE X bomb
                elif cell == -1:
                    # if the cell is a mine, draw an X in the cell
                    text = self.map_font.render("X", 1, "Red")
                    screen.blit(text, (
                    x + (cell_size / 2 - text.get_width() / 2), y + (cell_size / 2 - text.get_height() / 2)))

        # draw the info text about how many flags are left
        screen.blit(self.info_font.render("Flags:", 1, "white"), (10, 30))

        # color map the flag number so it changes color when running low
        if self.flags > 6:
            screen.blit(self.info_font.render(str(self.flags), 1, "green"), (10, 50))
        elif self.flags > 3:
            screen.blit(self.info_font.render(str(self.flags), 1, "yellow"), (10, 50))
        else:
            screen.blit(self.info_font.render(str(self.flags), 1, "red"), (10, 50))

        # refresh the display
        pygame.display.update()

    def check_cover(self, row, col):
        # check if the cell is a mine
        if self.solution_map[row][col] == -1 and self.cover_map[row][col] == 2:
            # if it is a mine, and you just marked it
            self.num_on_mines += 1
        elif self.solution_map[row][col] == -1 and self.cover_map[row][col] == 0:
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
                    # When there is a mouse click of some sort, get the position of the mouse and calibrate it to the board
                    click_row, click_col = self.get_calibrated_click_position(pygame.mouse.get_pos())
                    # print(click_col)
                    # if it is a left click
                    if event.button == 1:
                        # debugging position calibration
                        # print(click_row, click_col)
                        # if the click is outside of the board, do nothing
                        if click_row >= self.rows or click_col >= self.cols:
                            continue
                        # if it's the first move
                        if first_move:
                            # generate the map with the first click as the safe zone
                            self.generate_map(self.rows, self.cols, self.mines, click_row + 1, click_col + 1, 2)
                            # if self.solution_map[click_col + 1][click_row + 1] == -1:
                            #     self.first_move_map_update(click_col + 1, click_row + 1)
                            # not the first move anymore!
                            first_move = False
                        # if the cell is flagged give the flag back
                        if self.cover_map[click_col + 1][click_row + 1] == 2:
                            self.flags += 1
                        # reveal the cell
                        self.cover_map[click_col + 1][click_row + 1] = 1
                        # check if the cell is a mine
                        if self.solution_map[click_col + 1][click_row + 1] == -1:
                            # if it is a mine, and you just revealed it, you lose
                            self.game_lost = True
                        # reveal all the zeros around it
                        self.reveal_empty_spaces(click_col + 1, click_row + 1)

                    # only let players flag if it is not the first move
                    if not first_move:
                        if event.button == 3:
                            # debugging position calibration
                            # print(click_row, click_col)
                            # if the click is outside the board or already revealed, do nothing
                            if click_row >= self.rows or click_col >= self.cols or self.cover_map[click_col + 1][
                                click_row + 1] == 1:
                                continue
                            # if the cell is already flagged, unflag it
                            if self.cover_map[click_col + 1][click_row + 1] == 2:
                                self.cover_map[click_col + 1][click_row + 1] = 0
                                if not first_move:
                                    self.check_cover(click_col + 1, click_row + 1)
                                self.flags += 1
                            # if the cell is not flagged, flag it
                            elif self.flags > 0:
                                self.cover_map[click_col + 1][click_row + 1] = 2
                                if not first_move:
                                    self.check_cover(click_col + 1, click_row + 1)
                                self.flags -= 1
                            # if you ran out of flags, do nothing
                            elif self.flags == 0:
                                continue



            # self.print_map()
            # draw the mine
            self.draw_mine(screen, self.solution_map, self.cover_map)

            #win condition + lose condition checking
            if not first_move:
                # print(f"{self.num_on_mines}, {self.mines}")
                # if we have the same number of flags on mines as mines, check if we won
                # we won't run a win check if we haven't placed all the flags on the right mines yet
                if self.num_on_mines == self.mines:
                    # set our win variable to the result of the check
                    # the win check checks that all cells other than the marked ones are revealed
                    self.game_won = self.check_win()

                if self.game_won is True:
                    # if you won the game play the end screen with game won as true
                    time.sleep(0.3)
                    self.play_endscreen(True)
                if self.game_lost is True:
                    # if you lost the game play the end screen with game won as false
                    time.sleep(1)
                    self.play_endscreen(False)
            # flip() the display to put work on screen
            # pygame.display.flip()
            # clock.tick(60)
        pygame.quit()

    def check_win(self):
        # loop through the entire cover map except the gutters
        for i in range(1, len(self.cover_map) - 1):
            for j in range(1, len(self.cover_map[i]) - 1):
                # if the cell is not revealed and not marked, return False
                if self.cover_map[i][j] == 0:
                    print("found non-revealed cell")
                    if self.solution_map[i][j] != -1:
                        return False
        # if every cell is marked and not a mine + every other cell revealed return True
        return True

    def play_endscreen(self, win):
        # same display thing as before
        icon = pygame.image.load("Ericsweeper_thumb.png")
        pygame.display.set_icon(icon)
        screen = pygame.display.set_mode((1000, 800))
        win_font = pygame.font.Font("JetBrainsMono-VariableFont_wght.ttf", 55)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # if the user presses a key, check if it's y or n
                if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                    # if it's y, reset the game and play again
                    self.cover_map = np.zeros((self.cols + 2, self.rows + 2))
                    self.solution_map = np.zeros((self.cols + 2, self.rows + 2))
                    self.num_on_mines = 0
                    self.flags = self.mines
                    self.game_won = False
                    self.game_lost = False
                    self.play_game()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                    # if it's n, quit the game
                    pygame.quit()
                    sys.exit()

            # if this screen is entered with a win, display the win text, else display the lose text
            if win:
                text = win_font.render("You won!", 1, "white")
            else:
                text = win_font.render("You lost!", 1, "white")
            screen.blit(text, (500 - text.get_width() / 2, 400 - text.get_height() / 2))

            # display the continue text for the replayable loop
            continue_text = self.info_font.render("Play Again: Y   Quit: N", 1, "white")
            screen.blit(continue_text, (500 - continue_text.get_width() / 2, 600 - continue_text.get_height() / 2))

            pygame.display.update()


    def reveal_empty_spaces(self, y, x):
        # Create a deque to hold the locations to be cleared
        to_clear = deque([(y, x)])
        # To keep track of visited cells
        visited = set()
        # while our to clear is not empty, meaning we have zeros to clear
        while to_clear:
            # Pop the leftmost cell from the deque
            curr_y, curr_x = to_clear.popleft()
            # Check if the cell has already been visited
            if (curr_y, curr_x) in visited:
                continue

            # Add the current cell to the visited set if it is not
            visited.add((curr_y, curr_x))

            # Reveal the space at the current position
            self.cover_map[curr_y][curr_x] = 1

            # If the current cell in solution_map is 0, check its neighbors
            if self.solution_map[curr_y][curr_x] == 0:
                for dy, dx in self.relative_positions:
                    new_y, new_x = curr_y + dy, curr_x + dx

                    # Check for boundary conditions
                    if 0 <= new_y < self.solution_map.shape[0] and 0 <= new_x < self.solution_map.shape[1]:
                        # If the space at the new position is hidden
                        if self.cover_map[new_y][new_x] == 0:
                            # If it's an empty space or a number count, add to the deque
                            if self.solution_map[new_y][new_x] == 0 or self.solution_map[new_y][new_x] > 0:
                                to_clear.append((new_y, new_x))

    def get_calibrated_click_position(self, click_position):
        # get the x and y of the click
        click_x, click_y = click_position
        if self.rows > self.cols:
            # if the rows are bigger than the cols, then we have to calibrate the click position with these formulas
            cell_size = (self.width - 200) / self.rows
            col = click_y / cell_size - ((800 - cell_size * self.cols) / 2) / cell_size
            row = click_x / cell_size - ((1000 - cell_size * self.cols) / 2) / cell_size +(0.5*abs(self.rows-self.cols))
        else:
            # if the cols are bigger than the rows, then we have to calibrate the click position with these formulas
            cell_size = self.height / self.cols
            col = click_y / cell_size
            row = click_x / cell_size - ((1000 - cell_size * self.cols) / 2) / cell_size - (0.5*abs(self.rows-self.cols))

        # print(f"row: {row}, col: {col}")
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
                    user_argument[2]) > 21 or int(user_argument[1]) * int(user_argument[2]) < 25:
                print("Your grid is too long or too wide or too small, please try again.")
            elif int(user_argument[3]) > int(user_argument[1]) * int(user_argument[2]) - 25:
                print(f"You have too many mines, max number of mines is area - 25. Please try again.")
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
    minesweeper_controller = MinesweeperGM(user_width, user_height, user_num_mines)
    minesweeper_controller.flags = user_num_mines
    minesweeper_controller.mines = user_num_mines
    minesweeper_controller.play_intro()
    # minesweeper_controller.generate_map(user_width, user_height, user_num_mines)

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


"""
Peer Review Section:

Sebastian Plunkett' 24: play tested the early terminal-based version of the generation function

1. seems to be working, but nothing is accounting for creating very odd grids that are just bad to play on
2. i don't like this terminal interface

My revisions to this:

1. This is what prompted the code you now see in the main method of the code, the inputs are ran through very
through checks for all kinds of errors. This was critical to ensure the success of the game later on.
2. I made it into a pygame, Tada!

Leon Zhang '25: Play tested a very early pygame version of the game

1. add an intro video to the game to make it more accessible
2. there is a bug in your map generation where the bomb that gets moved to somewhere else isn't accounted for.

My revisions to this:
1. I made an intro video in After Effects in the style of this game. I also added a play_intro() method to the GM class
2. (note: this bug only existed in my previous way of "generating around the user click," the final version does not use this method
to avoid users clicking a bomb for their first move). I tweaked the look-around table and realized that I had not excluded
the gutters from being a place of random placement

Leon Zhang '25 (again): Final playtesting of a pygame version very close to the final version

1. The win condition works half the time
2. Your reveal_zeros works, but sometimes I still only just see the number I clicked on and nothing else
3. The mouse click position is calibrated when making a grid that is 14x16

My revisions to this:

1. I reworked the win condition, the previous way of checking had a bug where the grid changes during the middle of its
checking loop, causing the win to falsely trigger when not all spaces have been revealed yet
2. I reworked the entire generate_map() function to instead use a "safe_radius" and generate the map after the user's first click
3. I realized that I needed different functions to calculate the click position based on the grid's dimensions. This is 
because the alignment of the grid is very different when col > rows vs cols < rows. I implemented this into the calibration function
with conditionals

Ming Qin '25: Playtesting the Final Version:

This is more of an actual playtest than basic feedback. I said nothing else but to play the game. Ming was able to
play the game through with he proper interface and win. Furthermore, he was able to play another game without restarting
due to the new menu feature I implemented in the end screen.

Tye Chokephaibulkit '24: Long-term playtesting throughout development

1. found various small errors throughout the development process since he played many of my checkpoint versions
2. the most important bug found was in one of the early pygame versions where I put in the col and row index in the
wrong order so the whole map was actually messed up but it looked perfect when testing with squares.

My revisions to this:

1. fixed all the tiny errors found along the way
2. This was a great save, I would have never found this bug if it weren't for Tye's playtesting. I fixed it by putting
the indices in the right place. 

My Choate Singing Teacher (yes I sing): Adult playtesting

See, this is the "game of your elders," right? So I thought it would be a good idea to have an adult playtest the game.
It turned out that my singing teacher had played this game a lot during his childhood, so I was able to get feedback on 
the final version of the game and how everything felt. He really liked it, and in fact after seeing how this works, my
singing teacher wanted to learn some coding too!

And, finally, credit where credit's due: Google Minesweeper!

I used Google Minesweeper as sort of a reference benchmark for my game. Though there was no code, I did get how big my 
"safe_radius" should be from there.

"""