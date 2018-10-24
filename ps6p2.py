import math
import numpy as np
import sex
import orbit
from visual import *
from ephemPy import Ephemeris as Ephemeris_BC

class Ephemeris(Ephemeris_BC):

    def __init__(self, *args, **kwargs):
        Ephemeris_BC.__init__(self, *args, **kwargs)
        self.AUFAC = 1.0/self.constants.AU
        self.EMFAC = 1.0/(1.0+self.constants.EMRAT)

    def position(self, t, target, center):
        pos = self._position(t, target)
        if center != self.SS_BARY:
            pos = pos - self._position(t, center)
        return pos

    def _position(self, t, target):
        if target == self.SS_BARY:
            return numpy.zeros((3,), numpy.float64)
        if target == self.EM_BARY:
            return Ephemeris_BC.position(self, t, self.EARTH)*self.AUFAC
        pos = Ephemeris_BC.position(self, t, target)*self.AUFAC
        if target == self.EARTH:
            mpos = Ephemeris_BC.position(self, t, self.MOON)*self.AUFAC
            pos = pos - mpos*self.EMFAC
        elif target == self.MOON:
            epos = Ephemeris_BC.position(self, t, self.EARTH)*self.AUFAC
            pos = pos + epos - pos*self.EMFAC
        return pos

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


ephem = Ephemeris('405')
t_0 = 2457935.666667

#heliocentric position in ecliptic
sun_to_asteroid = vector(.244, 2.17, -.445)
#earth to sun in equitorial
earth_to_sun = ephem.position(t_0, 10, 2)
print earth_to_sun
#convert to ecliptic
earth_to_sun = rotate(earth_to_sun, -radians(23.437), vector(1,0,0))
print earth_to_sun
earth_to_asteroid = sun_to_asteroid + earth_to_sun
print earth_to_asteroid
earth_to_asteroid = earth_to_asteroid / (mag(earth_to_asteroid))
print "Eclip: ", toRADec(earth_to_asteroid)
eq = toRADec(rotate(earth_to_asteroid, radians(23.437), vector(1,0,0)))
print "Eq: ", toRADec(rotate(earth_to_asteroid, radians(23.437), vector(1,0,0)))
print "RA: ", sex.formatHMS(eq[0])
print "Dec: ", sex.formatDMS(eq[1])
