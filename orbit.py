from visual import *
import numpy as np
from ephemPy import Ephemeris as Ephemeris_BC


k = .01720209895
#c in AU per regular day
c = 173.1446
eps = 23.437


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

#makes x, y, z axes
def makeAxis(d, w = .03):
    xaxis = arrow(pos = (0,0,0), axis = (d,0,0), shaftwidth = w, color = color.blue)
    yaxis = arrow(pos = (0,0,0), axis = (0,d,0), shaftwidth = w, color = color.yellow)
    zaxis = arrow(pos = (0,0,0), axis = (0,0,d), shaftwidth = w, color = color.red)

#no pertubation acceleration
def accel(pos, mu = 1):
    return (-float(mu) *  pos) / float((mag(pos)**3))

#pos b is the object which pertubes the asteroid's position
def accelPer(pos, pos_b, mu_b = 1 ):
    return (-1 *  pos) / float((mag(pos)**3)) + (-mu_b * (pos - pos_b ) / float(mag(pos - pos_b)**3))


#pos is the position away from the center, v is the velocity relative to the center
#this method is done without pertubation
def RK4(pos, v, time_step):

    pos_1 = pos
    v_1 = v
    a_1 = accel(pos_1)

    pos_2 = pos + 0.5 * time_step * v_1
    v_2 = v + 0.5 * time_step * a_1
    a_2 = accel(pos_2)

    pos_3 = pos + 0.5 * time_step * v_2
    v_3 = v + 0.5 * time_step * a_2
    a_3 = accel(pos_3)

    pos_4 = pos + time_step * v_3
    v_4 = v + time_step * a_3
    a_4 = accel(pos_4)

    return pos + (v_1 + 2.0*v_2 + 2.0*v_3 + v_4)/6.0 * time_step, v +  (a_1 + 2.0*a_2 + 2.0*a_3 + a_4)/6.0 * time_step


def Euler(pos, v, time_step):

    v = v + accel(pos) * time_step
    return pos + v * time_step, v

#object b pertubes object a, mu_b is mass of b, replaces RK4 for pertubed objects
def preturb(a_position, b_position, a_velocity, time_step, mu_b = 1):
    pos = a_position
    v = a_velocity

    pos_1 = pos
    v_1 = v
    a_1 = accelPer(pos_1, b_position, mu_b)

    pos_2 = pos + 0.5 * time_step * v_1
    v_2 = v + 0.5 * time_step * a_1
    a_2 = accelPer(pos_2, b_position, mu_b)

    pos_3 = pos + 0.5 * time_step * v_2
    v_3 = v + 0.5 * time_step * a_2
    a_3 = accelPer(pos_3, b_position, mu_b)

    pos_4 = pos + time_step * v_3
    v_4 = v + time_step * a_3
    a_4 = accelPer(pos_4, b_position, mu_b)

    return a_position + (v_1 + 2.0*v_2 + 2.0*v_3 + v_4)/6.0 * time_step, a_velocity +  (a_1 + 2.0*a_2 + 2.0*a_3 + a_4)/6.0 * time_step

'''
@params
a_position - the object to be perturbed's position
a_velocity - the object to be perturbed's velocity
position_list - a list of positions of the objects perturbing the object
mass_list - a list of masses of the objects perturbing the object
'''
def preturb2(a_position, a_velocity, position_list, mass_list, time_step):
        pos = a_position
        v = a_velocity

        pos_1 = pos
        v_1 = v
        a_1 = accelPer2(pos_1, position_list, mass_list)

        pos_2 = pos + 0.5 * time_step * v_1
        v_2 = v + 0.5 * time_step * a_1
        a_2 = accelPer2(pos_2, position_list, mass_list)

        pos_3 = pos + 0.5 * time_step * v_2
        v_3 = v + 0.5 * time_step * a_2
        a_3 = accelPer2(pos_3, position_list, mass_list)

        pos_4 = pos + time_step * v_3
        v_4 = v + time_step * a_3
        a_4 = accelPer2(pos_4, position_list, mass_list)

        return a_position + (v_1 + 2.0*v_2 + 2.0*v_3 + v_4)/6.0 * time_step, a_velocity +  (a_1 + 2.0*a_2 + 2.0*a_3 + a_4)/6.0 * time_step


def accelPer2(pos, position_list, mass_list):
    accelSum = vector(0,0,0)
    for i in range(len(position_list)):
        accelSum += (-mass_list[i] * (pos - position_list[i])/float(mag(pos - position_list[i])**3))
    return accelSum

#gets the LST (in decimal as the fraction of the day)
def getLST(julian, longitude):
    julian -= 2451544.5
    sidereal = (1.0027379) * julian + .2773194444
    sidereal += longitude/(15.0 * 24)
    sidereal %= 1
    return sidereal


def toRADec(v):
    #finds the RA in degrees using the x and y coordinates
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
    #convert to degrees and make sure is positive
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

#returns a unit vector
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

#gets the classical orbital elements
def getOrbital(r, rdot):
    h = cross(r, rdot)

    print "Ang momentum: ", h

    e = cross(rdot, h) - (r)/(mag(r))

    print "Eccentricity: ", e

    print "Unit vector pointing towards perihelion: ", e/mag(e)

    a = (mag(h)**2)/(1-mag(e)**2)

    print "Semi-major axis: ", a
    print "Perihelion: ", a * (1-mag(e))

    inc = degrees(arccos(h.z/mag(h)))

    print "Inclination: ", inc

    N = cross(vector(0,0,1), h)

    if (N.y > 0):
        Omega = degrees(arccos(N.x / mag(N)))
    else:
        Omega = 360 - degrees(arccos(N.x / mag(N)))

    print "Ascending node", N
    print "Unit vector towards ascending node", N /(mag(N))
    print "Longitude of the ascending node: ", Omega

    if (e > 0):
        omega = degrees(arccos(dot(e, N)/(mag(e) * mag(N))))
    else:
        omega = 360 - degrees(arccos(dot(e, N)/ (mag(e) * mag(N))))

    print "Argument of perihelion: ", omega
