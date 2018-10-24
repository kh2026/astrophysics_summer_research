#Code to use EphemPy to get Rsun from JPL binary ephemeris tables

from visual import *
import numpy as np
import orbit
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


ephem = Ephemeris('405')

print ephem.position(2456858.791000, 10, 2)
print ephem.position(2455398.71717, 10, 2)

print "Earth to sun vector in eq. coordinates: ", (ephem.position(2457960.25, 10, 2))
print "New Haven to sun vector: ", -5.492560805490505E-01, 7.838554121995323E-01, 3.397883018659092E-01

t_0 = 2457960
#time step in days
t_step = .1
t = t_0

scene = display(center = (0,0,0))



sun = sphere(pos = (0,0,0), radius = .05, color = color.red )
mercury = sphere(pos = rotate(vector(ephem.position(t, 0, 10)), -radians(orbit.eps), (1,0,0)), radius = .01)
venus = sphere(pos = rotate(vector(ephem.position(t, 1, 10)), -radians(orbit.eps), (1,0,0)), radius = .01)
earth = sphere(pos = rotate(vector(ephem.position(t, 2, 10)), -radians(orbit.eps), (1,0,0)), radius = .001)
moon = sphere(pos = rotate(vector(ephem.position(t, 9, 10)), -radians(orbit.eps), (1,0,0)), radius = .0003)
mars = sphere(pos = rotate(vector(ephem.position(t, 3, 10)), -radians(orbit.eps), (1,0,0)), radius = .01)
jupiter = sphere(pos = rotate(vector(ephem.position(t, 4, 10)), -radians(orbit.eps), (1,0,0)), radius = .03)


mercury_trail = curve(pos = mercury.pos, color = color.red, retain = 10)
venus_trail = curve(pos = venus.pos, color = color.cyan, retain = 10)
earth_trail = curve(pos = earth.pos, color = color.blue, retain = 10)
moon_trail = curve(pos = moon.pos, color = color.orange, retain = 10)
mars_trail = curve(pos = mars.pos, color = color.magenta, retain = 10)
jupiter_trail = curve(pos = jupiter.pos, retain = 10)

orbit.makeAxis(2.5, .01)




while True:
    rate(100)
    mercury.pos = rotate(vector(ephem.position(t, 0, 10)), -radians(orbit.eps), (1,0,0))
    venus.pos = rotate(vector(ephem.position(t, 1, 10)), -radians(orbit.eps), (1,0,0))
    earth.pos = rotate(vector(ephem.position(t, 2, 10)), -radians(orbit.eps), (1,0,0))
    moon.pos = rotate(vector(ephem.position(t, 9, 10)), -radians(orbit.eps), (1,0,0))
    mars.pos = rotate(vector(ephem.position(t, 3, 10)), -radians(orbit.eps), (1,0,0))
    jupiter.pos = rotate(vector(ephem.position(t, 4, 10)), -radians(orbit.eps), (1,0,0))

    mercury_trail.append(mercury.pos)
    venus_trail.append(venus.pos)
    earth_trail.append(earth.pos)
    moon_trail.append(moon.pos)
    mars_trail.append(mars.pos)
    jupiter_trail.append(jupiter.pos)


    scene.center = earth.pos




    t += t_step
