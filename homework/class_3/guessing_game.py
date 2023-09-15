"""
Eric
September 14th, 2023
Sources:
I used the rich text library to style terminal output - https://rich.readthedocs.io/en/latest/introduction.html

Reflection:
I think this was a nice assignment to review basic control flow and python ints. I took this opportunity to learn how to
present my python program's better with the rich text library. I also improved my in-code documentation by documenting
each method with a docstring. Overall, fantastic second assignment!

On my honor, I have neither given nor received unauthorized aid on this assignment.
"""

import random
import time
from rich import print as rprint
import os
from erictools.ezinput import EZInputHandlerUser


class MathHost:
    def __init__(self, l_bound, u_bound, step):
        self.lower_bound = l_bound
        self.upper_bound = u_bound
        self.step = step
        self.random_number = 0
        self.ez_input = EZInputHandlerUser("Eric")

    def change_lower_bound(self, new_l_bound):
        '''
        This function changes the lower bound of the random number generator
        :param new_l_bound: The new lower bound
        :return: Noting
        '''
        self.lower_bound = new_l_bound

    def change_upper_bound(self, new_u_bound):
        '''
        This function changes the upper bound of the random number generator
        :param new_u_bound: The new upper bound
        :return: Nothing
        '''
        self.upper_bound = new_u_bound

    def change_step(self, new_step):
        '''
        This function changes the step of the random number generator
        :param new_step: The new step
        :return: Nothing
        '''
        self.step = new_step

    def generate_random_number(self):
        '''
        This function generates a random number between the lower and upper bounds
        :return: Nothing
        '''
        return random.randrange(self.lower_bound, self.upper_bound, self.step)

    def play_game(self):
        '''
        This function is the main game loop
        :return: Nothing
        '''
        os.system('clear')
        rprint("[bright_white]What number do you want to start at?[/bright_white]")
        self.change_lower_bound(int(input(">>>")))
        rprint("[bright_white]What number do you want to end at?[/bright_white]")
        self.change_upper_bound(int(input(">>>")))
        rprint("[bright_white]What number do you want to increment by?[/bright_white]")
        self.change_step(int(input(">>>")))
        time.sleep(0.5)
        rprint("[bright_magenta]Ok! Let's start the game[/bright_magenta]")
        time.sleep(0.5)
        os.system('clear')
        self.random_number = self.generate_random_number()
        rprint("[bright_white]I'm thinking of a number between " + str(self.lower_bound) + " and " + str(self.upper_bound) + "[/bright_white]")
        time.sleep(0.5)
        for i in range(4):
            if i == 3:
                rprint("[bright_white]The number was " + str(self.random_number) + "[/bright_white]")
                time.sleep(0.5)
                rprint("[bright_white]Unfortunately, you didn't guess the number![/bright_white]")
                break
            elif i == 2:
                rprint("[bright_blue]You have 1 guess left![/bright_blue]")
            guess = int(input("Enter your guess\n>>>"))
            if self.check_answer(guess):
                rprint("[bright_green]Correct![/bright_green]")
                time.sleep(0.5)
                rprint("[bright_green]You win![/bright_green]")
                time.sleep(0.5)
                break
            else:
                if guess > self.random_number:
                    rprint("[bright_red]Too high![/bright_red]")
                    time.sleep(0.5)
                else:
                    rprint("[bright_red]Too low![/bright_red]")
                    time.sleep(0.5)
        play_again = input("Do you want to play again? (y/n)\n>>>")
        if play_again.lower().strip() == 'y':
            self.play_game()
        else:
            rprint("[bright_white]Ok, thanks for playing![/bright_white]")

    def check_answer(self, answer):
        '''
        This function checks if the user's answer is correct
        :param answer: user input answer
        :return: True if answer is correct, False if answer is incorrect
        '''
        return answer == self.random_number

    def introduce_game(self):
        '''
        This function introduces the game to the user
        :return: Nothing
        '''
        # change this base on OS
        os.system('clear')

        rprint("[bright_white]Welcome to the [bold bright_magenta]Guessing Game[/bold bright_magenta]![/bright_white]")
        time.sleep(1)
        print("In this game, you will be given a random number between a lower and upper bound.")
        demo_number = 0
        for i in range(49):
            demo_number = random.randrange(1, 100, 1)
            print("\r" + str(demo_number), end="")
            time.sleep(0.02)
        print()
        time.sleep(1)
        print("Your job is to guess the number!")
        time.sleep(1)
        guess_demo_number = 0
        for i in range(49):
            guess_demo_number = random.randrange(1, 100, 1)
            if guess_demo_number == demo_number:
                guess_demo_number = random.randrange(1, 100, 1)
            print("\r" + str(guess_demo_number), end="")
            time.sleep(0.02)
        print()
        if guess_demo_number > demo_number:
            rprint("[bold bright_red]Too high![/bold bright_red]")
        else:
            rprint("[bold bright_red]Too low![/bold bright_red]")
        time.sleep(1)
        print("If you guess incorrectly, you will be told whether your guess is too high or too low.")
        time.sleep(1)
        if demo_number > 18:
            range_start_demo = demo_number - 18
        else:
            range_start_demo = 0
        for i in range(range_start_demo, demo_number):
            print("\r" + str(i), end="")
            time.sleep(0.02)
        print()
        time.sleep(0.1)
        rprint("[bold bright_green]Correct![/bold bright_green]")
        print("If you guess the number correctly, you win!")
        time.sleep(2)
        print()
        rprint("[bright_magenta]You will be given 3 guesses to guess the number correctly.[/bright_magenta]")
        print()
        time.sleep(1)
        ready_to_start = input("Are you ready to play? (y/n)\n>>>")
        time.sleep(0.3)
        if ready_to_start.lower().strip() == 'y':
            self.play_game()
        else:
            print("Ok, let's go through the instructions again.")
            time.sleep(0.5)
            self.introduce_game()


if __name__ == "__main__":
    problem_host = MathHost(0, 100, 1)
    problem_host.introduce_game()

