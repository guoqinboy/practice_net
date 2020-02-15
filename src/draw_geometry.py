# 几何图形
import time
from turtle import *
# speed(0)
width(4)
bgcolor('#ee6b97')
color('white')
title('美丽的几何图案')
def dbx(n):
    for i in range(1,n+1):
        forward(200)
        left(360/n)
def dbxs(m):
    for j in range(1,m+1):
        dbx(4)
        left(360/m)

dbxs(8)


time.sleep(3)