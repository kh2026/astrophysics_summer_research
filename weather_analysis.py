from astropy.io import ascii
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

def sin_model(data, amp, period, phase, yint):
    return amp * np.sin(((data + phase) * 2 * np.pi) / float(period) ) + yint



f = open("/home/student/python/data/Condition_Sunrise-newhaven.csv")

weather_info = ascii.read(f, names = ["Date/Time", "Average_Temperature", "Skies", "High", "Low"])

#get JD list  of the weather info
julian_d = pd.DatetimeIndex(weather_info["Date/Time"])
julian_d = julian_d.to_julian_date()


def model_temperature():
    plt.plot(julian_d, weather_info["High"], '.', label = "High", color = "red")
    plt.plot(julian_d, weather_info["Low"], '.', label = "Low", color = "blue")

    x = np.linspace(2456200, 2458000, 1800)
    model_params = 50, 365, 20, 50
    plt.plot(x, sin_model(x, *model_params), color = "green")


    plt.xlabel( "Julian Date" )
    plt.ylabel( "Temperature" )

    plt.show()

    print "RMS of residuals for High:", math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, *model_params) )))
    print "RMS of residuals for Low:", math.sqrt(np.mean(np.square( weather_info["Low"] - sin_model(julian_d, *model_params) )))


def best_season():
    skies = weather_info["Skies"]
    date = weather_info["Date/Time"]

    summercount, fallcount, wintercount, springcount = 0, 0, 0, 0

    for index, e in enumerate(date):
        if ("June" in e or "July" in e or "August" in e) and (skies[index] == "Clear" or skies[index] == "Fair"):
            summercount += 1
        if ("September" in e or "October" in e or "November" in e) and (skies[index] == "Clear" or skies[index] == "Fair"):
            fallcount += 1
        if ("December" in e or "January" in e or "February" in e) and (skies[index] == "Clear" or skies[index] == "Fair"):
            wintercount += 1
        if ("March" in e or "April" in e or "May" in e) and (skies[index] == "Clear" or skies[index] == "Fair"):
            springcount += 1

    summerdays = [e for e in date if ("June" in e or "July" in e or "August" in e)]
    falldays = [e for e in date if ("September" in e or "October" in e or "November" in e)]
    winterdays = [e for e in date if ("December" in e or "January" in e or "February" in e)]
    springdays = [e for e in date if ("March" in e or "April" in e or "May" in e)]

    print "Summer percentage: ", 100 * summercount/float(len(summerdays)), "Fall percentage: ", 100 *  fallcount/float(len(falldays)), \
    "Winter percentage: ", 100 * wintercount/float(len(winterdays)), "Spring percentage: ", 100 * springcount/float(len(springdays))
    print "Summer is the best season for observing"




def optimize_model():
    possible_models = [(amp, period, phase, yint) for amp in np.linspace(20,30, 11) for period in  np.linspace(360,370, 11) for phase in  np.linspace(5,15, 11) \
    for yint in  np.linspace(50,60,11) ]
    min_residual = 100000000
    for i in range(len(possible_models)):
        residual = math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, *possible_models[i]))))
        if residual < min_residual:
            min_residual = residual
            best_model = possible_models[i]
    print "The RMS of the residuals with the best model is : ", min_residual
    print "This occurs with amp = ", best_model[0], " degrees, period = ", best_model[1], "days, phase = ", best_model[2], "days shifted, yint = ", best_model[3], "degrees."

    plt.plot(julian_d, weather_info["High"], '.', label = "High", color = "red")
    x = np.linspace(2456200, 2458000, 1800)
    plt.plot(x, sin_model(x, *best_model), color = "green")
    plt.xlabel( "Julian Date" )
    plt.ylabel( "Temperature" )
    plt.show()


def gradient_climb():
    #initial params
    parameters = (23, 363, 6, 60)
    step_size = .1

    def find_next(step_size, params):
        best_direction = [0,0,0,0]
        print params
        best_residual = math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, *params))))
        print math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, 23, 363, 6, 60))))
        print math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, 23.1, 363.1, 6.001, 60.001))))
        direction_set =  [(amp, period, phase, yint) for amp in [-1,1] for period in [-1,1] for phase in  [-1,1] \
        for yint in [-1,1] ]


        print direction_set


        amp, period, phase, yint = parameters
        for direction in direction_set:
            testamp, testperiod, testphase, testyint = amp + direction[0]*step_size, period + direction[1]*step_size, phase + direction[2]*step_size,\
            yint + direction[3]*step_size
            params = testamp, testperiod, testphase, testyint
            residual = math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, testamp, testperiod, testphase, testyint))))
            print residual
            if residual < best_residual:
                best_direction = direction
                best_residual = residual
        print best_direction, best_residual

    find_next(.01,parameters)


    '''
    min_residual = 1000
    for i in range(len(possible_models)):
        residual = math.sqrt(np.mean(np.square( weather_info["High"] - sin_model(julian_d, *possible_models[i]) )))
        if residual < min_residual:
            min_residual = residual
            best_model = possible_models[i]
    print "The Chi-Sq of the residuals with the best model is : ", residual
    print "This occurs with amp = ", best_model[0], " degrees, period = ", best_model[1], "days, phase = ", best_model[2], "days shifted, yint = ", best_model[3], "degrees."

    plt.plot(julian_d, weather_info["High"], '.', label = "High", color = "red")
    x = np.linspace(2456200, 2458000, 1800)
    plt.plot(x, sin_model(x, *best_model), color = "green")
    plt.xlabel( "Julian Date" )
    plt.ylabel( "Temperature" )
    plt.show()

    '''

gradient_climb()
