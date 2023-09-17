"""
Eric
September 14th, 2023
Sources:
I used the rich text library to style terminal output - https://rich.readthedocs.io/en/latest/introduction.html
I copied some code from my Markov Chain music model research project to save high scores to a pickle file
I built (and technically "used") the ezinput library to handle user input

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
from erictools.ezinput import EZInputHandlerBase
import pickle


class MathHost:
    def __init__(self, l_bound, u_bound, step):
        self.lower_bound = l_bound
        self.upper_bound = u_bound
        self.step = step
        self.random_number = 0
        self.ez_input = EZInputHandlerBase()
        self.player_name = ""

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
        try:
            return int(random.randrange(self.lower_bound, self.upper_bound, self.step))
        except ValueError:
            rprint("[bright_red]Invalid bounds, please try again.[/bright_red]")
            time.sleep(0.5)
            self.configure_bounds()

    def configure_bounds(self):
        os.system('clear')
        self.change_lower_bound(self.ez_input.handle_int_input("What number do you want to start at?"))
        self.change_upper_bound(self.ez_input.handle_int_input("What number do you want to end at?"))
        self.change_step(self.ez_input.handle_int_input("What number do you want to increment by?"))

    def configure_player(self):
        os.system('clear')
        rprint("[bright_white]What is your name?[/bright_white]")
        self.player_name = input(">>>")
        rprint(f"[bright_white]Ok, {self.player_name}, let's get started![/bright_white]")
        time.sleep(0.5)

    def add_new_score(self, score):
        # <--------This was ripped & modified from my Markov Chain music model research project-------->
        with open('guess_game_highscores.pkl', 'rb') as f:
            scores = pickle.load(f)
        new_score_entry = {"name": self.player_name, "score": score}
        scores.append(new_score_entry)
        scores.sort(key=lambda x: x["score"], reverse=True)
        with open('guess_game_highscores.pkl', 'wb') as f:
            pickle.dump(scores, f)

    def play_game(self):
        '''
        This function is the main game loop
        :return: Nothing
        '''
        self.configure_player()
        self.configure_bounds()
        score = 0
        time.sleep(0.5)
        first_round_guesses = 20
        game_lost = False
        game_lost, guesses_used = self.single_round(first_round_guesses)
        while game_lost is False:
            score += 1
            print(f"You currently have {score} points.")
            time.sleep(3)
            game_lost, guesses_used = self.single_round(guesses_used)
        print(f"Game over! You scored {score} points!")
        self.add_new_score(int(round((score * (self.upper_bound - self.lower_bound)) / 2)))
        print("Do you want to play again?")
        play_again = self.ez_input.handle_bool_input()
        if play_again:
            self.play_game()
        else:
            rprint("[bright_white]Ok, thanks for playing![/bright_white]")

    def single_round(self, guesses):
        self.random_number = self.generate_random_number()
        rprint("[bright_magenta]Ok! Let's start the game[/bright_magenta]")
        time.sleep(0.5)
        os.system('clear')
        rprint("[bright_white]I'm thinking of a number between " + str(self.lower_bound) + " and " + str(
            self.upper_bound) + "[/bright_white]")
        time.sleep(0.5)
        for i in range(guesses):
            if i == guesses - 1:
                rprint("[bright_white]The number was " + str(self.random_number) + "[/bright_white]")
                time.sleep(0.5)
                rprint("[bright_white]Unfortunately, you didn't guess the number![/bright_white]")
                return True, i + 1
            elif i == guesses - 2:
                rprint("[bright_blue]You have 1 guess left![/bright_blue]")
            else:
                rprint("[bright_blue]You have " + str(guesses - i) + " guesses left![/bright_blue]")
            play_game = self.ask_guess(i)
            if play_game is not None:
                return play_game
            # try:
            #     self.ask_guess(i)
            # except TypeError:
            #     rprint("[bright_red]Invalid input, please try again.[/bright_red]")
            #     time.sleep(0.5)
            #     self.ask_guess(i)

    def ask_guess(self, i):
        guess = self.ez_input.handle_int_input("Enter your guess:")
        print("got past guess handler")
        if self.check_answer(guess):
            rprint("[bright_green]Correct![/bright_green]")
            time.sleep(0.5)
            rprint("[bright_green]You win![/bright_green]")
            time.sleep(0.5)
            return False, i + 1
        else:
            if guess > self.random_number:
                rprint("[bright_red]Too high![/bright_red]")
                time.sleep(0.5)
            else:
                rprint("[bright_red]Too low![/bright_red]")
                time.sleep(0.5)
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
        time.sleep(1)
        print("If you guess the number correctly, you win!")
        time.sleep(2)
        os.system('clear')
        rprint("[bright_magenta]You will be given 20 guesses to guess the number correctly initially.[/bright_magenta]")
        print()
        time.sleep(2)
        rprint("[bright_magenta]Next round, you must guess the number in less rounds[/bright_magenta]")
        print()
        time.sleep(2)
        rprint("[bright_magenta]You will be allowed less and less guesses[/bright_magenta]")
        print()
        time.sleep(2)
        rprint("[bright_magenta]Your final score will be calculated with: correct_rounds * interval / increment[/bright_magenta]")
        print()
        time.sleep(2)
        rprint("[bright_magenta]Basically, your score will be higher the wider your range & smaller the increment[/bright_magenta]")
        print()
        time.sleep(3)
        with open('guess_game_highscores.pkl', 'rb') as f:
            highscores = pickle.load(f)
        print(f"{highscores[0]['name']} has the highest score of {highscores[0]['score']}!")
        time.sleep(1)
        print("Are you ready to play?")
        ready_to_start = self.ez_input.handle_bool_input()
        time.sleep(0.3)
        if ready_to_start:
            self.play_game()
        else:
            print("Ok, let's go through the instructions again.")
            time.sleep(0.5)
            self.introduce_game()


if __name__ == "__main__":
    problem_host = MathHost(0, 100, 1)
    problem_host.introduce_game()
