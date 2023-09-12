"""
Eric Yang25
September 12th, 2023

Sources:
I learned about and used the ASCII art module from to present prettier nicknames: https://pypi.org/project/art/
I used Textblob for basic sentimental analysis to aid in the creation of the infinite interaction loop:
https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis
Polarity score reading I did to learn more about how to set my polarity thresholds for positive and negative
emotions: https://www.red-gate.com/simple-talk/development/data-science-development/sentiment-analysis-python/
I used ChatGPT to generate the different story cutout templates with empty names and adjectives


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
        interaction_choice = input("1. Get a joke, 2. Get a random question, 3. Get a really, really horrible story XD")
        if interaction_choice == 1:
            self.give_joke()
        elif interaction_choice == 2:
            self.give_rand_question()
        elif interaction_choice == 3:
            pass


    def analyze_emotion(self, response):
        blob_analyzer = TextBlob(response)
        polarity = blob_analyzer.sentiment.polarity
        # USE PRINT FOR TUNING ONLY
        print(polarity)
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

    def give_rand_question(self):
        print(random.choice(self.random_questions))
        print(self.analyze_emotion(input(">>>")))

    def y_n_handler(self):
        choice = input("(y/n)\n").lower
        if choice == "y":
            return True
        else:
            return False


if __name__ == "__main__":
    first_name = input("Hello! What is your first name?\n>>>")
    main_greeter = Greeter(first_name)
    print(f"Hey {first_name}!")
    nickname_condition = input("Do you want a nickname? (y/n)\n>>>").lower()
    if nickname_condition == "y":
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
    time.sleep(2)
    want_joke = input("Do you want to hear a joke? (y/n)\n>>>").lower()
    if want_joke == "y":

    print("I'm going to ask you some random questions now!")
    while True:
        main_greeter.interaction()
        keep_going = input("Do you want to keep talking? (y/n)\n>>>")
        if keep_going == "n":
            print("Bye! Thanks for using my program!")
            break

