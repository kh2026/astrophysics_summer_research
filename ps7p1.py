from astropy.io import ascii
from visual import *
import matplotlib.pyplot as plt
#-*- coding: ASCII -*-

f = open("/home/student/python/data/arduino-logger-data-balloon.TXT")

t_elapse, tilt, alt, temp, accel = [], [], [], [], []
geiger_data = []


for line in f.readlines():
    if line[0].isdigit():
        d_1, d_2, d_3, d_4, d_5, d_6, d_7, d_8, d_9 =(line.split(", "))
        t_elapse.append(float((d_1)))
        tilt.append(vector(float(d_2), float(d_3), float(d_4)))
        alt.append(d_5)
        temp.append(d_6)
        accel.append(vector(float(d_7), float(d_8), float(d_9)))
    if line[0] == "C" and len(line.split(", ")) == 7:
        geiger_data.append(line)




accel = [mag(vector) for vector in accel]
t_elapse = [(t * .001) - 1500 for t in t_elapse]

usv_hr = []
for line in geiger_data:
    usv_hr.append((line.split(", ")[5]))

print type(alt), type(usv_hr),   len(alt), len(usv_hr), len(alt[0:7400:74]), len(usv_hr[0:6800:68])
'''
#alt vs t
plt.plot(t_elapse, alt, '.', label = "Altitude vs. Time Elapsed", color = "red")
plt.xlabel( "Time Elapsed [s]" )
plt.ylabel( "Altitude [m]" )
plt.title("Altitude vs. Time Elapsed")
plt.show()

#temp vs alt
plt.plot()
plt.plot(alt, temp, '.', label = "Temperature vs. Altitude", color = "blue")
plt.xlabel( "Altitude [m]" )
plt.ylabel( "Temperature [C]" )
plt.title("Temperature vs. Altitude")
plt.show()
'''

#radiation vs alt
plt.plot()
plt.plot(alt[0:7400:74], usv_hr[0:6800:68], ".",  label = "uSv/Hr vs. Altitude", color = "green")
plt.xlabel( "Altitude [m]" )
plt.ylabel( "uSv/Hr" )
plt.title("Altitude vs. uSv/Hr")
plt.show()

'''
#accel vs t
plt.plot()
plt.plot(t_elapse, accel,  label = "Acceleration vs. Time Elapsed", color = "black")
plt.xlabel( "Time Elapsed [s]" )
plt.ylabel( "Acceleration [m/s^2]" )
plt.title("Acceleration vs. Time Elapsed")
plt.show()
'''
