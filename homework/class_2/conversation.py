"""
Eric Yang25
September 12th, 2023

Sources:
I learned about and used the ASCII art module from to present prettier nicknames: https://pypi.org/project/art/
I used Textblob for basic sentimental analysis to aid in the creation of the infinite interaction loop:
https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis
Polarity score reading I did to learn more about how to set my polarity thresholds for positive and negative
emotions: https://www.red-gate.com/simple-talk/development/data-science-development/sentiment-analysis-python/
I used ChatGPT to generate the  story cutout templates with empty names and adjectives
I used numpy for the Ericsweeper thing: https://numpy.org/doc/stable/reference/arrays.ndarray.html


I think this is a great introductory assignment, I did something similar to this during spring of last year
when I took CS570. I wanted the greeter to be able to interact with the user for as long as the user wanted,
so I focused on designing a greeter program that had a loop-able function that would ask the user simple and
random questions. I also wanted to make the program more interesting by adding a VERY basic, but nonetheless
fun nickname generator. Overall,I  enjoyed doing this :)

On my honor, I have neither given nor received unauthorized aid on this assignment.
"""

import random
from art import tprint
from textblob import TextBlob
import time
import numpy as np


class Greeter:
    def __init__(self, user_name):
        self.name = user_name
        self.suffixes = ["ster", "y", "inator", "meister", "o", "ie", "zilla", "bear"]
        self.random_questions = ["How are you today?", "How is school going for you?", "How's your week been going?",
                                 "What are your feelings about school?", "Describe how you are feeling right now.",
                                 "Describe how tired you have been in the last week?", "How was your weekend?",
                                 "How are your friends?"]
        self.random_jokes = ["What do you call a fake noodle?",
                             "What do you call an alligator in a vest?",
                             "What do you call a pile of cats?",
                             "What do you call a pig that does karate?",
                             "What do you call a cow with no legs?",
                             "What do you call a cow with two legs?",
                             "What do you call a cow with all legs?",
                             "What do you call a cow that just gave birth?"]
        self.random_jokes_ans = ["Impasta!", "An Investigator!", "A Meowtain!", "A Pork Chop!", "Ground Beef!",
                                 "Lean Beef!", "High Steaks!", "De-calf-inated!"]


    def interaction(self):
        interaction_choice = input("1. Get a joke, 2. Get a random question, 3. Get a really, really horrible story XD, 4. Play Ericsweeper\n>>>")
        if interaction_choice == '1':
            self.give_joke()
        elif interaction_choice == '2':
            self.give_rand_question()
        elif interaction_choice == '3':
            self.tell_horrible_story()
        elif interaction_choice == '4':
            self.play_ericsweeper()
        else:
            print("Oops! That's not an option!")

    def play_ericsweeper(self):
        sweep_board = np.zeros((10, 10), int)
        for i in range(len(sweep_board)):
            for j in range(len(sweep_board[i])):
                sweep_board[i][j] = random.randint(0, 2)

        print("Welcome to Ericsweeper, the worst version of minesweeper you can play!")
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
        continue_game = True
        while continue_game is True:
            if sweep_board[pos_y][pos_x] == 0 or pos_y == previous_y and pos_x == previous_x:
                print("You've stepped on safe grounds!")
            elif sweep_board[pos_y][pos_x] == 1:
                print("You've gained +1 immunity!")
                immunity += 1
                sweep_board[pos_y][pos_x] = 0
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

    def analyze_emotion(self, response):
        blob_analyzer = TextBlob(response)
        polarity = blob_analyzer.sentiment.polarity
        # USE PRINT FOR TUNING ONLY
        #print(polarity)
        # this can be fine-tuned further to be more accurate with the sentiment analysis
        if polarity > 0.5:
            return "That's amazing to hear!"
        elif polarity > 0.2:
            return "That's great to hear!"
        elif polarity > 0:
            return "One of those regular days, huh?"
        elif polarity > -0.5:
            return "I hope you feel better soon!"
        else:
            return "No matter what is going on right now, know that everything will be okay!"

    def make_nickname(self):
        if len(self.name) <= 3:
            return "Sorry! Your name is too short"
        else:
            front_two_head = self.name[:2].lower()
            rand_suffix = random.choice(self.suffixes)
            nickname = f"{front_two_head}{rand_suffix}"
            return nickname.capitalize()

    def give_joke(self):
        # we need an index number to get the joke ans so we cant just use random.choice()
        random_joke_index = random.randint(0, len(self.random_jokes))
        print(self.random_jokes[random_joke_index])
        time.sleep(0.8)
        print("Think you got the answer? Press enter to see!")
        input()
        print(self.random_jokes_ans[random_joke_index])
        time.sleep(0.6)

    def give_rand_question(self):
        print(random.choice(self.random_questions))
        print(self.analyze_emotion(input(">>>")))

    def y_n_handler(self):
        choice = input("(y/n)\n>>>")
        choice.lower()
        if choice == "y":
            return True
        else:
            return False

    def tell_horrible_story(self):
        # should probably optimize this in the future with loops and better story data stroage
        print("Alright...just don't come crying back when this story sucks XD")
        time.sleep(0.6)
        person_1 = input("Give me a name\n>>>")
        person_2 = input("Give me another name\n>>>")
        person_3 = input("Give me another name\n>>>")
        verb_1 = input("Give me a verb\n>>>")
        verb_2 = input("Give me another verb\n>>>")
        verb_3 = input("Give me another verb\n>>>")
        verb_4 = input("Give me another verb\n>>>")
        verb_5 = input("Give me another verb\n>>>")
        adjective_1 = input("Give me a adjective\n>>>")
        adjective_2 = input("Give me another adjective\n>>>")
        adjective_3 = input("Give me another adjective\n>>>")
        adjective_4 = input("Give me another adjective\n>>>")
        adjective_5 = input("Give me another adjective\n>>>")
        print(f"Once upon a time in a {adjective_1} forest, there lived three best friends named {person_1}, {person_2}, and {person_3}. They were known for their {adjective_2} friendship and {adjective_3} adventures.")
        time.sleep(0.8)
        print(f"One fine day, they decided to {verb_1} to the mysterious cave on the edge of the forest. It was said that the cave was home to a {adjective_4} treasure.")
        time.sleep(0.8)
        print(f"As they {verb_2} into the depths of the cave, {person_1} felt a {adjective_5} sensation. Something was not right. Just then, {person_2} managed to {verb_3} a hidden trap door in the floor.")
        time.sleep(0.8)
        print(f"\"Quick!\" shouted {person_3}, \"We need to {verb_4} before it's too late!\"")
        time.sleep(0.8)
        print(f"And so, they did. Avoiding the trap, they moved further and found the treasure glittering in the dim light.")
        time.sleep(0.8)
        print(f"\"{person_1}, you were right. This is {adjective_3}!\" exclaimed {person_2}.")
        time.sleep(0.8)
        print(f"The three friends {verb_5} the treasure and returned home, their hearts full of joy and their friendship stronger than ever.")
        time.sleep(0.8)
        print(f"And so, in the {adjective_1} forest, the three friends lived happily, always ready for a new adventure.")


if __name__ == "__main__":
    first_name = input("Hello! What is your first name?\n>>>")
    main_greeter = Greeter(first_name)
    print(f"Hey {first_name}!")
    time.sleep(0.9)
    print("Do you want a nickname?")
    if main_greeter.y_n_handler() is True:
        print(f"Your nickname is:")
        tprint(main_greeter.make_nickname())
    else:
        print("Okay! No nickname for you!")
    print("How are you doing today?")
    print(main_greeter.analyze_emotion(input(">>>")))
    home_town = input("Where are you from?\n>>>").lower().strip()
    if home_town == "vancouver" or home_town == "van":
        print("No way! I'm from Vancouver too!")
    else:
        print("Nice to know!")
    time.sleep(1)
    print("Do you want to hear a joke?")
    if main_greeter.y_n_handler() is True:
        main_greeter.give_joke()
    else:
        print("Guess you are not in humor, huh?")
    time.sleep(0.9)
    print("Now it's your turn, you can ask me to do these things")
    while True:
        main_greeter.interaction()
        keep_going = input("Do you want to keep talking? (y/n)\n>>>")
        if keep_going == "n":
            print("Bye! Thanks for using my program!")
            break

