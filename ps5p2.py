import math
import numpy as np
from visual import *

#RA in hours, Dec in degrees
def toXYZ(RA, Dec):

    #the z coordinate of the z vector is sin(Dec)
    Dec = math.radians(Dec)
    z = math.sin(Dec)

    #convert the RA in hours to radians
    RAdeg = 15 * RA
    RArad = math.radians(RAdeg)

    #l = sqrt(x^2 + y^2) , x^2 + y^2 + z^2 = 1
    l = math.sqrt( 1 - z*z)

    x = l * math.cos(RArad)
    y = l * math.sin(RArad)

    v = vector(x, y, z)
    return v


b = toXYZ(195.27/15., 40.02)
n = toXYZ(162.93/15., 41.31)

print n, b
print math.degrees(arccos(dot(n, b)))
print mag(b-n) * 6371
print b-n
ntob = b-n

ntoasteroid = 149597871 * .3 / 6371. * n
btoasteroid = ntoasteroid + ntob
print ntoasteroid
print btoasteroid

print degrees(arccos(dot(ntoasteroid, btoasteroid)/(mag(ntoasteroid)*mag(btoasteroid))))
