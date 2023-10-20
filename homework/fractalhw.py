"""
Eric
October 19th, 2023

Sources:
About trees observing golden ratio - https://www.sciencedirect.com/science/article/pii/S1002007108003419#:~:text=Although%20trees%20and%20bushes%20differ,the%20ratio%20is%201%3A0.618.

Reflection:
Recursion for drawing seems fun, I am already thinking of what other cool things I can draw with turtle. Funnily enough
I actually used the fibonacci sequence in this project to determine how much to shrink the tree by. This was achieved by
taking the standard formula for the golden ratio and solving for the ratio of the smaller to larger segment. Recursion
was implemented by drawing the baseline of the tree, then calling the function again with the new length and a new scale
to shrink the tree by. This was done 5 times, and the result is a pretty cool looking tree. I also added a beach and water
just for fun.

Have a good day! :)

On my honor, I have neither given nor received unauthorized aid on this assignment.
"""

import turtle
import math

# golden ratio
shrink_factor = 1 + math.sqrt(5) / 2

# turtle setup
turtle.speed(0)
turtle.tracer(100, 0)

# initialize 800x800 turtle tk window
screen = turtle.Screen()
screen.title("Hi Ms. Healey :)")
screen.setup(800, 800)


# define the recursive function
def repeating_tree(scale, direction, x, y):
    # base case
    if scale < 8:
        return

    # set color
    if scale > 20:
        turtle.color('brown')
    else:
        turtle.color('forest green')

    # recursive case
    turtle.pensize(scale / 200)

    # draw the tree "line" in specific direction
    turtle.penup()
    turtle.setheading(direction)
    # pick up from the end of last base "line"
    turtle.goto(x, y)
    turtle.pendown()
    turtle.forward(scale - 10)

    # calculate next x and y and also the next scale
    next_x = turtle.xcor()
    next_y = turtle.ycor()
    new_scale = scale / shrink_factor

    # draw 5 branches in different directions
    repeating_tree(new_scale, direction + 20, next_x, next_y)
    repeating_tree(new_scale, direction - 20, next_x, next_y)
    repeating_tree(new_scale, direction + 50, next_x, next_y)
    repeating_tree(new_scale, direction - 50, next_x, next_y)
    repeating_tree(new_scale, direction, next_x, next_y)


def beach():
    turtle.penup()
    turtle.goto(-400, -400)
    turtle.pendown()
    turtle.color('sandy brown')
    turtle.begin_fill()
    turtle.forward(800)
    turtle.left(90)
    turtle.forward(200)
    turtle.left(90)
    turtle.forward(800)
    turtle.left(90)
    turtle.forward(200)
    turtle.end_fill()


def water():
    turtle.penup()
    turtle.goto(-400, -200)
    turtle.pendown()
    turtle.color('light blue')
    turtle.begin_fill()
    turtle.forward(800)
    turtle.left(90)
    turtle.forward(200)
    turtle.left(90)
    turtle.forward(800)
    turtle.left(90)
    turtle.forward(200)
    turtle.end_fill()


if __name__ == "__main__":
    beach()
    water()
    repeating_tree(350, 90, 0, -300)
    turtle.exitonclick()
