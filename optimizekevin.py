import time
start = time.time()

from astropy.io import ascii
#takes 4s
import numpy as np

import math

import pandas as pd
#takes .7s

def sin_model(data, amp, period, phase, yint):
    return amp * np.sin(((data + phase) * 2 * np.pi) / float(period) ) + yint

f = open("/home/student/python/data/Condition_Sunrise-newhaven.csv")

weather_info = ascii.read(f, names = ["Date/Time", "Average_Temperature", "Skies", "High", "Low"])



julian_d = pd.DatetimeIndex(weather_info["Date/Time"])
julian_d = julian_d.to_julian_date()
#2s



def gradient_climb():
    #initial params
    params = (20, 365, 3, 50)
    best_residual = math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, *params))))
    step_size = 10
    count = 0
    while time.time() - start < 60:
        amp = np.random.normal(params[0], step_size)
        period = np.random.normal(params[1],step_size)
        phase = np.random.normal(params[2], step_size)
        yint = np.random.normal(params[3], step_size)
        residual  = math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, amp, period, phase, yint))))
        if residual < best_residual:
            best_residual = residual
            params = amp, period, phase, yint
            count = 0
        else:
            count += 1

        if count > 1000:
            step_size /= 10.

    print step_size
    print "amp, period, phase, yint:", params
    print "smallest rms:", best_residual


gradient_climb()
