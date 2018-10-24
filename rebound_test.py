import rebound
import math
import numpy as np
from visual import *

sim = rebound.Simulation()


for i in range(5):
    x = np.random.uniform(-1, 1)
    y = np.random.uniform(-1, 1)
    z = 0
    m = np.random.uniform(0, 1)
    vx = np.random.uniform(-.01, .01)
    vy = np.random.uniform(-.01, .01)
    vz = np.random.uniform(-.01, .01)

    sim.add(m = m, x = x, y = y, z = z, vx = vx, vy = vy, vz = vz)

scene = display(x = 0, y= 0, width = 5, height = 5, center = (0,0,0))
particles = sim.particles

p = []
p_c = []
for  index, particle in enumerate(particles):
    p.append(sphere(radius = particle.m / 10., pos = vector(particle.x, particle.y, particle.z), color = (np.random.uniform(0, 1,3))))
    p_c.append(curve(pos = p[index].pos, retain = 3, color = p[index].color ))


t_count = 0
t_step = 0.01




while(True):
    rate(100)
    sim.integrate(t_count)
    t_count += t_step

    for index, particle in enumerate(particles):
        p[index].pos = vector(particle.x, particle.y, particle.z)
        p_c[index].append(pos = p[index].pos)
