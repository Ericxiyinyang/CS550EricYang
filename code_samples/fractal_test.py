import turtle
import math

screen = turtle.Screen()
screen.setup(1000,1000)
screen.setworldcoordinates(-1000,-1000,1000,1000)
turtle.speed(0)
golden_ratio = (1+5**0.5)/2
turtle.tracer(0,0)
def golden_fractal_tree(x,y,direction,length):
    turtle.up()
    turtle.goto(x,y)
    turtle.seth(direction)
    turtle.pensize(math.log(length,2)/3)
    if length<10: turtle.color('forest green')
    else: turtle.color('gray')
    turtle.down()
    turtle.fd(length)
    if length < 3: return
    # cx,cy = turtle.xcor(), turtle.ycor()
    # golden_fractal_tree(cx,cy,direction+72,(2-golden_ratio)*length)
    # golden_fractal_tree(cx,cy,direction-72,(2-golden_ratio)*length)
    # golden_fractal_tree(cx,cy,direction,(golden_ratio-1)*length)

golden_fractal_tree(0,-900,90,700)
turtle.update()

turtle.exitonclick()
