import rebound
import math
import numpy as np
import time as t
import matplotlib.pyplot as plt
import orbit
start = t.time()

sim = rebound.Simulation()

#get r and r dot in ecliptic
tx68_r = (0.6139644063, -1.0965881191, -0.2116846217)
tx68_rdot = (0.9654570616, 0.4011235326, -0.1276785091)
time = 2457952.6433

#add 2002TX68
sim.add(m = 0, x = tx68_r[0], y = tx68_r[1], z = tx68_r[2], vx = tx68_rdot[0], vy = tx68_rdot[1], vz = tx68_rdot[2])


sim.add(m = 1, x = 2.665842519136602E-03, y = 5.211742206599118E-03, z =-1.403063885389406E-04, \
 vx = 0, vy = 0, vz = 0)
sim.add(m = 3.003E-6, x = 4.397590615594086E-01, y =-9.122840820283953E-01, z =-1.014885247182010E-04,\
 vx = 1.525256572068380E-02, vy = 7.336377539094126E-03, vz =-1.651429457614512E-07)
sim.add(m = 9.541E-4, x =-4.909522601553919E+00, y =-2.354719664424277E+00, z = 1.195758746918782E-01,\
 vx= 3.175680530322254E-03, vy =-6.446783002391737E-03, vz =-4.427991847450773E-05)

particles = sim.particles



t_count = 0
t_step = 1

t_arr = []
distance_arr = []

closest = math.sqrt( (particles[0].x - particles[2].x)**2 + (particles[0].y - particles[2].y) ** 2 + (particles[0].z - particles[2].z) **2)
closest_time = 0

sim.integrate(17308.53)
sim.status()


'''
while t_count < :
    sim.integrate(t_count)
    t_count += t_step

    asteroid_distance =  math.sqrt( (particles[0].x - particles[2].x)**2 + (particles[0].y - particles[2].y) ** 2 + (particles[0].z - particles[2].z) **2)
    if   asteroid_distance < closest:
        closest = asteroid_distance
        closest_time = t_count
    distance_arr.append(asteroid_distance)
    t_arr.append(t_count)
    print t_count

print "closest distance, closest time:", closest, closest_time
print "time ran (mod day)", t_count

for i in range(len(t_arr)):
    t_arr[i] = t_arr[i] / orbit.k

plt.plot(t_arr, distance_arr,  color = "green", label = "Asteroid to Earth Distance")
plt.xlabel( "Time [JD past 1/1/2017]" )
plt.ylabel( "Distance [AU]" )
plt.title("Asteroid to Earth Distance")
plt.show()
'''
