import time
from turtle import *
# draw_polygon.py
  

shape('turtle')
bgcolor('#ee6b97')
width(5)
speed(0)
def draw_poly(n,step):
    color('green') # green  purple red
    for i in range(n):
        forward(step)
        left(360/n)

def draw_polies(m):
    for j in range(m):   
        draw_poly(6,100)
        left(360/m)

draw_polies(20) # m 多少个多边形

time.sleep(4)

def draw_square():
    title('正方形螺旋')
    bgcolor('#e93e36')
    pencolor('white')
    speed(0)
    for i in range(1,120):
        forward(i*4)
        left(90)
    hideturtle()

# draw_square()
