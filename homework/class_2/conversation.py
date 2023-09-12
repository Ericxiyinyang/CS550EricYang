"""
Eric Yang25
September 12th, 2023

Sources:
I learned about and used the ASCII art module from to present prettier nicknames: https://pypi.org/project/art/
I used Textblob for basic sentimental analysis to aid in the creation of the infinite interaction loop:
https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis
Polarity score reading I did to learn more about how to set my polarity thresholds for positive and negative
emotions: https://www.red-gate.com/simple-talk/development/data-science-development/sentiment-analysis-python/


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

    def interaction(self):
        print(random.choice(self.random_questions))
        print(self.analyze_emotion(input(">>>")))

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
    print("I'm going to ask you some random questions now!")
    while True:
        main_greeter.interaction()
        keep_going = input("Do you want to keep talking? (y/n)\n>>>")
        if keep_going == "n":
            print("Bye! Thanks for using my program!")
            break

