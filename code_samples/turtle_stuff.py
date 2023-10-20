import turtle
import math

# turtle.penup()
# turtle.setpos(-300, 60)
# turtle.pendown()
# #draw "E"
# turtle.forward(110)
# turtle.right(90)
# turtle.forward(50)
# turtle.right(90)
# turtle.forward(50)
# turtle.left(90)
# turtle.forward(30)
# turtle.left(90)
# turtle.forward(50)
# turtle.right(90)
# turtle.forward(50)
# turtle.right(90)
# turtle.forward(50)
# turtle.left(90)
# turtle.forward(30)
# turtle.left(90)
# turtle.forward(50)
# turtle.right(90)
# turtle.forward(50)
# turtle.right(90)
# turtle.forward(110)
# turtle.right(90)
# turtle.forward(210)

# let's draw a spiral with recursion

def spiral(size):
    # draw a round spiral, NOT a square spiral
    if size < 1:
        return
    turtle.forward(size / 10)
    turtle.right(10)
    turtle.forward(size / 10)
    turtle.right(10)
    turtle.forward(size / 10)
    turtle.right(10)
    turtle.forward(size / 10)
    turtle.right(10)
    turtle.forward(size / 10)
    turtle.right(10)
    turtle.forward(size / 10)
    turtle.right(10)
    turtle.forward(size / 10)
    turtle.right(10)
    turtle.forward(size / 10)
    turtle.right(10)
    spiral(size - 5)

turtle.pensize(2)
turtle.penup()
spiral_size = 300
turtle.setpos(spiral_size/(math.pi*math.pi) + 80, 50)
turtle.pendown()

turtle.speed(0)
turtle.tracer(100, 0)


for i in range(21):
    spiral(spiral_size)
    turtle.right(90)
    turtle.forward(spiral_size)




turtle.exitonclick()