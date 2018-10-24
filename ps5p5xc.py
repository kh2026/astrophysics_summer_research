from visual import *
import orbit

orbit.makeAxis(3, .02)


time = 0
time_delta = .01

sun = sphere(pos = vector(0,0,0), radius = .25)
earth = sphere(pos = vector(1,0,0), radius = .08, color = color.red)
asteroid = sphere(pos = vector(.9,0,0), radius = .05, color = color.blue)
jupiter = sphere(pos = vector(5,0,0), radius = .12, color = color.orange )

earth_curve = curve(color = color.red, )
asteroid_curve = curve(color = color.blue, )
jupiter_curve = curve(color = color.orange, )

earth_V = vector(0, 1, 0)
asteroid_V = vector(0, 1.3, 0)
jupiter_V = vector(0, .5, 0)

preturb_masses = [1, .005, .5]

min_distance = mag(earth.pos-asteroid.pos)
years = 100

while(True):
    rate(45)


    earth.pos, earth_V = orbit.RK4(earth.pos, earth_V, time_delta)
    jupiter.pos, jupiter_V = orbit.RK4(jupiter.pos, jupiter_V, time_delta)

    preturb_positions = [vector(0,0,0), earth.pos, jupiter.pos]


    asteroid.pos, asteroid_V = orbit.preturb2(asteroid.pos, asteroid_V, preturb_positions, preturb_masses, time_delta)

    time += time_delta
    earth_curve.append(earth.pos)
    jupiter_curve.append(jupiter.pos)

    asteroid_curve.append(asteroid.pos)



    #find collision points
    if (mag(asteroid.pos-earth.pos) < .01):
        collision_point = sphere(pos = asteroid.pos, radius = .01, color = color.orange)

    #time_label = label(pos = vector(1.5,1.5,0), height = .1, text = "T = {} ".format(time),)
