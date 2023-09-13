import numpy as np
import random

sweep_board = np.zeros((10, 10), int)
for i in range(len(sweep_board)):
    for j in range(len(sweep_board[i])):
        sweep_board[i][j] = random.randint(0, 2)

print("Welcome to Ericsweeper, the worst version of minesweeper you can play!")
pos_x = random.randint(0, len(sweep_board[1])-1)
pos_y = random.randint(0, len(sweep_board)-1)

# if you are started under a bomb you get moved to somewhere with no bomb under
while sweep_board[pos_y][pos_x] == 2:
    for i in range(len(sweep_board)):
        for j in range(len(sweep_board[i])):
            pos_x = j
            pos_y = i
previous_x = pos_x
previous_y = pos_y
immunity = 0
continue_game = True
while continue_game is True:
    if sweep_board[pos_y][pos_x] == 0 or pos_y == previous_y and pos_x == previous_x:
        print("You've stepped on safe grounds!")
    elif sweep_board[pos_y][pos_x] == 1:
        print("You've gained +1 immunity!")
        immunity += 1
    else:
        if immunity > 0:
            immunity -= 1
            print("You've stepped on a landmine, but don't worry you still have immunity!")
            print(f"Current Immunity Left: {immunity}")
        else:
            print("Game Over!")
            continue_game = False
            break
    previous_x = pos_x
    previous_y = pos_y
    direction = input("1. up, 2. down, 3. right, 4. left\n>>>")
    if direction == '1':
        if pos_y == 0:
            print("Can't move up anymore! choose another direction")
        else:
            pos_y -= 1
    elif direction == '2':
        if pos_y == 9:
            print("Can't move down anymore! choose another direction")
        else:
            pos_y += 1
    elif direction == '3':
        if pos_x == 9:
            print("Can't move right anymore! choose another direction")
        else:
            pos_x += 1
    elif direction == '4':
        if pos_x == 0:
            print("Can't move left anymore! choose another direction")
        else:
            pos_x -= 1
    else:
        print("Oops! That's not an option!")
