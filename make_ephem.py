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


'''
@params
t_0 Julidan days
t_f Julian days
latitude degrees
longitude degrees (W of PM is negative)
r_0 in equitorial
rdot_0 in equitorial
tau_step in mod days

returns RA and Dec in degrees
'''
def make_ephem(t_0, t_f, r_0, rdot_0, tau_step = .00001, latitude = None, longitude = None):

    #get earth to sun vector in AU, equitorial coordinates
    def get_geocentric(lat, lst):
        gg = 0.000042587504556 * vector(cos(radians(lat))*cos(radians(lst*360)), cos(radians(lat))* sin(radians(lst*360)), sin(radians(lst*360)))
        return vector(gg)



    #find the final earth_to_sun vector in equitorial
    R_f = vector(ephem.position(t_f, 10, 2))
    #correct for position on earth
    if latitude  and longitude:
        R_f = R_f - get_geocentric(latitude, orbit.getLST(t_f, longitude))


    #find the amount of time to be elapsed
    tau_0 = 0
    tau_f = (t_f - t_0) * orbit.k
    tau = tau_0

    #RK4 integrate position and velocity
    r = r_0
    rdot = rdot_0
    #corrects if final time is earlier than given time
    if tau_f < tau_0:
        while(tau  > tau_f ):
            r, rdot = orbit.RK4(r, rdot, -tau_step )
            tau -= tau_step
    else:
        while(tau  < tau_f ):
            r, rdot = orbit.RK4(r, rdot, tau_step )
            tau += tau_step
    r_f = r

    #fundamental triangle
    rho_f = R_f + r_f

    #speed of light correction
    t_f = t_f - mag(rho_f)/orbit.c


    #redo with corrected time
    #find the final earth_to_sun vector in equitorial
    R_f = vector(ephem.position(t_f, 10, 2))
    #correct for position on earth
    if latitude and longitude:
        R_f = R_f - get_geocentric(latitude, orbit.getLST(t_f, longitude))


    tau_0 = 0
    tau_f = (t_f - t_0) * orbit.k
    tau = tau_0
    #RK4 integrate position and velocity
    r = r_0
    rdot = rdot_0
    if tau_f < tau_0:
        while(tau  > tau_f ):
            r, rdot = orbit.RK4(r, rdot, -tau_step )
            tau -= tau_step
    else:
        while(tau  < tau_f ):
            r, rdot = orbit.RK4(r, rdot, tau_step )
            tau += tau_step
    r_f = r

    #fundamental triangle
    rho_f = R_f + r_f
    ##end speed of light correction

    #convert to RA/Dec
    RA, Dec = orbit.toRADec(rho_f)

    #print final

    return RA, Dec




'''
@params:
t_0 in Julian day
t_f in Julian day
r_0 in heliocentric equitorial
rdot_0 in heliocentric equitorial
tau_step in modified day
'''
def make_ephem_nogeo(t_0, t_f, r_0, rdot_0, tau_step = .00001):


    #find the amount of time to be elapsed
    tau_0 = 0
    tau_f = (t_f - t_0) * orbit.k
    tau = tau_0

    #find the final earth_to_sun vector in equitorial
    R_f = ephem.position(t_f, 10, 2)
    print R_f
    #correct for position on earth

    #RK4 integrate position and velocity
    r = r_0
    rdot = rdot_0
    while(tau  < tau_f ):
        r, rdot = orbit.RK4(r, rdot, tau_step )
        tau += tau_step
    r_f = r

    #fundamental triangle
    rho_f = R_f + r_f
    #convert to RA/Dec
    RA, Dec = orbit.toRADec(vector(rho_f))


    #print "Rho Final:", rho_f
    print "RA: ", sex.formatHMS(RA)
    print "Dec: ", sex.formatDMS(Dec)
    return RA, Dec



if __name__ == '__main__':
    print make_ephem(t_0 =  2457940.666666, t_f = 2457935.666666, latitude = 41.3083, longitude = -72.9279, r_0 = vector(.244, 2.17, -.445), rdot_0 = vector (-.731, .0041, .0502))
