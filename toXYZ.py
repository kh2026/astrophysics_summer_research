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




#converts from x,y,z coordinates to ecliptic coordinates x,y,z
def toEclip(v):
    v = rotate(v, math.radians(-23.437), vector(1,0,0) )
    return v



#converts from Ecliptic x,y,z to ecliptic RA and Dec
def toRADec(v):
    #finds the RA  in radians using the x and y coordinates
    if v.x == 0:
        if v.y > 0:
            RA = math.pi / 2
        else:
            RA = 3 * math.pi/2
    else:
        RA = np.arctan(v.y/v.x)
    #adds pi rad if x<0 because arctan can only give between -pi/2 and pi/2
    if (v.x < 0):
        RA += math.pi
    #convert to hours and make sure is positive
    RA = math.degrees(RA)

    if(RA<0):
        RA += 360

    #finds the dec based on the ratio of the z coordinate and the planar length
    if (v.z == 1):
        Dec = math.pi/2
    else:
        Dec = np.arctan(v.z/math.sqrt(v.x * v.x + v.y * v.y))
    if (Dec < 0):
        Dec += 2 * math.pi
    Dec = math.degrees(Dec)

    return RA, Dec

#coordinates of 2002 TX68
TX68RA = 20 + 14/60.0 + 41.12/3600
TX68Dec = 29 + 47/60.0 + 53.4/3600

"""
print toRADec(toEclip(toXYZ(TX68RA, TX68Dec)))
print toXYZ(TX68RA, TX68Dec)
print toEclip(toXYZ(TX68RA, TX68Dec))
"""

print toXYZ(18 + 37/60., 38 + 47/60.)
