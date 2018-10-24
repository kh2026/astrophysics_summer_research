from visual import *
import numpy as np

asteroid_r = vector(0.244, 2.17, -0.445)
asteroid_rdot = vector(-0.731, -0.0041, 0.0502)

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


getOrbital(asteroid_r, asteroid_rdot)
