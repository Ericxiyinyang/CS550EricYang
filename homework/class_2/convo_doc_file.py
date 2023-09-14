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
        self.suffixes = ["..."]
        self.random_questions = ["..."]
        self.random_jokes = ["..."]
        self.random_jokes_ans = ["..."]


    def interaction(self):
        pass

    def play_ericsweeper(self):
        pass

    def analyze_emotion(self, response):
        pass

    def make_nickname(self):
        pass
    def give_joke(self):
        pass

    def give_rand_question(self):
        pass

    def y_n_handler(self):
       pass

    def tell_horrible_story(self):
        pass


if __name__ == "__main__":
    pass

