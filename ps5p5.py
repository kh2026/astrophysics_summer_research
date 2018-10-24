from visual import *

k = .01720209895

time = 0
time_delta = .01
sun = sphere(pos = vector(0,0,0), radius = .25)
planetE = sphere(pos = vector(.9,0,0), radius = .05, color = color.red)
planetRK = sphere(pos = vector(.677,-1.58,-.437), radius = .05, color = color.blue)
planet_trailE = curve (color = color.red, )
planet_trailRK= curve (color = color.blue, )
planet_V_E = vector(0, 1.485, 0)
planet_V_RK = vector(-1.73, 7.43, .8198)


def accel(pos):
    return (-1. *  pos) / float((mag(pos)**3))


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


flag = False
flag2 = False
while(True):
    rate(10000)


    planetE.pos, planet_V_E = Euler(planetE.pos, planet_V_E, time_delta)
    planetRK.pos, planet_V_RK = RK4(planetRK.pos, planet_V_RK, time_delta)

    time += time_delta
    planet_trailE.append(planetE.pos)
    planet_trailRK.append(planetRK.pos)


    if(abs((mag(planetRK.pos) - mag(planetE.pos))/mag(planetRK.pos)) > .01) and not flag:
        print "time: ", time
        flag = True

    if abs(planetE.pos.y) < .01 and not flag2:
        print planetE.pos, planet_V_E
        flag2 = True
