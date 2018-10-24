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




ephem = Ephemeris('405')

t_f = 2457940.666666

tau_0 = 0
tau_f = 5 * orbit.k
tau_step = .00001
tau = tau_0

R_f = rotate(ephem.position(t_f, 10, 2), -radians(orbit.eps), vector(1,0,0))

#find the geocentric vector in ecliptic coordinates
def get_geocentric(lat, lst):
    g_eclip = 0.000042587504556 *vector(cos(radians(lat))*cos(radians(lst*360)), cos(radians(lat))* sin(radians(lst*360)), sin(radians(lst*360)))
    g_eclip = rotate(g_eclip, -radians(orbit.eps), vector(1,0,0))
    return g_eclip

R_f = R_f - get_geocentric(41.3083, orbit.getLST(t_f, -72.9279))

print R_f 
r_0 = vector(.244, 2.17, -.445)
rdot_0 = vector (-.731, .0041, .0502)

r = r_0
rdot = rdot_0

while(tau  < tau_f ):
    r, rdot = orbit.RK4(r, rdot, tau_step )
    tau += tau_step

r_f = r
print r_f, rdot
rho_f = R_f + r_f



#convert to equitorial
rho_f = rotate(rho_f, radians(orbit.eps), vector(1,0,0))
#convert to RA/Dec
RA, Dec = orbit.toRADec(rho_f)



print "R_final:", R_f
print "RA: ", sex.formatHMS(RA)
print "Dec: ", sex.formatDMS(Dec)
