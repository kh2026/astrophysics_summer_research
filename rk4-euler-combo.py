# A program to integrate a two body orbit given an initial
# position and velocity.  Numerical integration by Runge-Kutta 4.

from visual import *
import math

mu = 1.0
k = 0.01720209895

# Here are the initial conditions

# MFFA
r = vector(0.9, 0.000001, 0.)
rdot = vector (0, 1.3, 0.)

rE = vector(0.9, 0.000001, 0)
rEdot = vector(0, 1.3, 0)



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


delta_t = 0.01
time = 0.
delta_r = 0.

while delta_r/mag(r) < 0.01:
     state = rk4(r, rdot, a, delta_t)
     r = state[0]
     rdot = state[1]
     
     rEdot = rEdot - (mu*rE/mag(rE)**3)*delta_t  #Equation of motion
     rE = rE + rEdot*delta_t
    
    #print 'time = ', time, 'r = ', r, 'r_dot = ', rdot 
     time = time + delta_t
     delta_r = abs(mag(r) - mag(rE))
     #print "delta_r", delta_r
    


print 'time = ', time, 'r = ', r, 'r_dot = ', rdot
print 'mag(r) = ', mag(r)
print 'time = ', time, 'rE = ', rE, 'r_dot = ', rEdot
print 'mag(rE) = ', mag(rE)
    
