from visual import *
import matplotlib.pyplot as plt

#J(t), R(t), dJ/dt, dR/dt,
J = 0
R = 1
Jdot = 0
Rdot = 0


t = 0

#visualizes J(t) and R(t)
Jsphere = sphere(pos = (-5, 0, 0), radius = 2, color = color.red)
Rsphere = sphere(pos = (5, 0, 0), radius = 2, color = color.blue)
axis = box(pos = (0,0,0), height = .1, length = 10, width = 10)

#used for plot
Rlist = []
Jlist = []
Tlist = []

while (t < 3000):
    rate(1000)

    #differential equations for dJ/dt and dR/dt
    Rdot = J * .01
    Jdot = -R * .1

    R += Rdot
    J += Jdot

    Jsphere.pos = (-5, J, 0)
    Rsphere.pos = (5, R, 0)

    t += 1

    #keep track of the points
    Rlist.append(R)
    Jlist.append(J)
    Tlist.append(t)

#plot the points
plt.scatter( Tlist, Rlist, color = color.blue)
plt.scatter( Tlist, Jlist, color = color.red)
plt.show()
