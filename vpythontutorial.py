from visual import *
import numpy as np
import datetime
import time


now = datetime.datetime.now()


timeH = now.hour
timeM = now.minute
timeS = now.second


#hours to radians from 12:00
timeH = radians(timeH * 30)
axisH = (sin(timeH), cos(timeH), 0)

timeM = radians(timeM * 6)
axisM = (1.5 * sin(timeM), 1.5 * cos(timeM), 0)

timeS = radians(timeS * 6)
axisS = (2 * sin(timeS), 2 * cos(timeS), 0)

m = arrow(pos = (0,0,0), axis =  axisM, shaftwidth = .05)
h = arrow(pos =(0,0,0), axis = axisH, color = color.blue, shaftwidth = .05)
s = arrow(pos = (0,0,0), axis =  axisS, color = color.red, shaftwidth = .04)

rOut = ring(pos = (0,0,0), axis = (0,0,1), radius = 2, thickness = .02, color = color.cyan)
rIn = ring(pos = (0,0,0), axis = (0,0,1), radius = .04, thickness = .02, color = color.white)
label(text = '12', pos = (0,1.8,0), color=color.green)

while(True):
    rate(50)


    s.axis = rotate(s.axis,-radians(6),(0,1,1))
    m.axis = rotate(m.axis,-radians(6/30.0),(1,1,0))
    h.axis = rotate(h.axis,radians(6/90.0),(1,0,1))
    rOut.axis = rotate(rOut.axis,radians(6),(0,1,1))
