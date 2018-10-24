#2017-Aug-03
import numpy as np
from visual import *

observed_mag = 16.68
sun_to_ast = vector(8.136709851212512E-01, -9.309267607602065E-01, 1.204893933933754E-01)
sun_to_earth = vector(6.606926299374440E-01, -7.701299292865856E-01, 2.627737262556596E-05)
earth_to_ast =  vector(1.529783551838071E-01, -1.607968314736209E-01, 1.204631160207498E-01)

def phase_angle(sun_to_ast, sun_to_earth):
    phase_angle = degrees(np.arccos(np.dot(sun_to_ast, sun_to_earth)/((mag(sun_to_ast)*mag(sun_to_earth)))))
    return phase_angle

def reduced_mag(observed_mag, sun_to_ast, earth_to_ast):
    reduced_mag = observed_mag - 5 * np.log(mag(sun_to_ast)*mag(earth_to_ast))
    return reduced_mag

def absolute_mag(reduced_mag,phase_angle):
    A1 = 3.33
    A2 = 1.87
    B1 = 0.63
    B2 = 1.22
    G = 1.5
    phi1 = np.exp((-A1 * ((np.tan(0.5*radians(phase_angle))) ** B1)))
    phi2 = np.exp((-A2 * ((np.tan(0.5*radians(phase_angle))) ** B2)))
    abs_mag = reduced_mag + 2.5 * np.log((1-G)*phi1 + G*phi2)
    return abs_mag

reduced_mag = reduced_mag(observed_mag, sun_to_ast, earth_to_ast)
phase_angle = phase_angle(sun_to_ast, sun_to_earth)
print "Phase angle in degrees: ", phase_angle
print "Reduced Magnitude: ", reduced_mag
print "Absolute Magnitude: ", absolute_mag(reduced_mag,phase_angle)

