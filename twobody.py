from visual import *
#time step

time = .05

#create sun and planet
sun = sphere(pos = vector(0,0,0), radius = 50, color = color.yellow)
planet = sphere(pos = vector(0,150, 0), radius = 20, color = color.white)
planet_trail = curve(color = color.blue)
sun_trail = curve(color = color.red)

#initial velocity of the bodies
planet_V = vector(.5,0,0)
sun_V = vector(0,-.01,0)
distance = mag(planet.pos - sun.pos)

while(True):
    rate(10000)

    #mass of sun is 10x the mass of planet
    #set acceleration
    planet_VDot = (500 *  (sun.pos - planet.pos)) / (distance**3) * time
    sun_VDot = (50 * (planet.pos - sun.pos)) / (distance**3) * time

    #set motion of planet and sun
    planet.pos = planet.pos + planet_V * time
    planet_V = planet_V + planet_VDot * time

    sun.pos = sun.pos + sun_V * time
    sun_V = sun_V + sun_VDot * time


    distance = mag(planet.pos - sun.pos)


    sun_trail.append(sun.pos)
    planet_trail.append(planet.pos)
