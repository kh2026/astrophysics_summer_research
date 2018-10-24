from visual import *
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

k = 0.01720209895
mu = 1

def a(x, v, dt):
    #Two-body acceleration law.  Can sub in other force laws
    return -1.*(mu/mag(x)**3)*x
    #Spring Law
    #return -1.*r


def rk4(x, v, a, dt):
	x1 = x
	v1 = v
	a1 = a(x1, v1, 0)

	x2 = x + 0.5*v1*dt
	v2 = v + 0.5*a1*dt
	a2 = a(x2, v2, dt/2.0)

	x3 = x + 0.5*v2*dt
	v3 = v + 0.5*a2*dt
	a3 = a(x3, v3, dt/2.0)

	x4 = x + v3*dt
	v4 = v + a3*dt
	a4 = a(x4, v4, dt)

	xf = x + (dt/6.0)*(v1 + 2*v2 + 2*v3 + v4)
	vf = v + (dt/6.0)*(a1 + 2*a2 + 2*a3 + a4)

	return xf, vf

orbit.makeAxis(2)
ephem = Ephemeris('405')
t_start = 2457952.6433

sun  = sphere( radius = .2)
tx68 = sphere(pos = vector(.622857, -1.10846, -.206566), radius = .05, color = color.red)
tx682 = sphere( pos = vector(8.279564617058560E-01,-9.222168167246064E-01,1.161042833829486E-01), radius = .05)
tx682rdot = vector(1.422218882841535E-02,8.781054904451557E-03,-4.394147584146805E-03)/orbit.k
earth = sphere(pos = vector(ephem.position(t_start, 2, 10)), radius = .1, color = color.green)
tx68rdot =  vector(1.01478, 0.338304, -0.109409)

tx682trail = curve(pos = tx682.pos)
tx68trail = curve(pos = tx68.pos, color = color.red)
earthtrail = curve(pos = earth.pos, color = color.green)

t = t_start

dt = .01 * k

while(True):
    rate(100000)
    tx68.pos, tx68rdot = rk4(tx68.pos, tx68rdot, a, dt)
    tx682.pos, tx682rdot = rk4(tx682.pos, tx682rdot, a, dt)
    earth.pos = (ephem.position(t, 2, 10))
    tx68trail.append(tx68.pos)
    earthtrail.append(earth.pos)
    tx682trail.append(tx682.pos)
    t += dt / k
