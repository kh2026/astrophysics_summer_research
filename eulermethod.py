from visual import *

time = .05
sun = sphere(pos = vector(0,0,0), radius = 50)
planet = sphere(pos = vector(0,150, 0), radius = 20)
planet_trail = curve (color = color.red, )

planet_V = vector(1.2,0,0)

while(True):

    rate(10**10)
    planet.pos = planet.pos + planet_V * time
    planet_VDot = (-5000 * planet.pos) / (mag(planet.pos)**3) * time
    planet_V = planet_V + planet_VDot * time




    planet_trail.append(planet.pos)
