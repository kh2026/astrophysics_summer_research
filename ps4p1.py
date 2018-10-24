import matplotlib.pyplot as plt
import numpy as np
import math

#finds the line of best fit with least squrae method
def bestFit(x, y):

    #this is the numerator for the slope
    def crossSum(x,y):
        n = float(len(x))
        crossSum = 0
        for i in range(len(x)):
            crossSum += (x[i] - np.sum(x)/n) * (y[i] - np.sum(y)/n)
        return crossSum

    ySum = np.sum(y)
    xSum = np.sum(x)
    n = float(len(x))
    yAvg = ySum / n
    xAvg = xSum / n

    #this is the denominator for the sloep
    def denom(x,y):
        denom = 0
        for i in range(len(x)):
            denom += (x[i] - xAvg) ** 2
        return denom

    m = crossSum(x, y) / denom(x,y)
    b = (ySum - m * xSum) / n
    print "m: ", m, "b: ", b
    return m, b


def printResiduals(x, y, m, b):
    for i in range(len(x)):
        print "The residual for x = ", x[i], "is ", y[i] - m * x[i] - b


#finds the standard deviation of the residuals for a given fit
def sigma(x,y,m,b):
    residuals = np.array([])
    for i in range(len(x)):
        residuals = np.append(residuals, y[i] - m * x[i] - b)

    mean = sum(residuals) / float(len(residuals))

    numerator = 0
    for i in range(len(residuals)):
        numerator += (residuals[i] - mean) ** 2

    sigma = math.sqrt(numerator / float(len(residuals)))
    return sigma


#this is the scatter plot with the line of best fit for all data
xValues = np.array([1.1, 1.6, 2.0, 2.1, 2.9, 3.2, 3.3, 4.4, 4.9])
yValues = np.array([72.61, 72.91, 73.00, 73.11, 73.52, 73.70, 76.10, 74.26, 74.51])
plt.scatter(xValues, yValues )
m, b = bestFit(xValues, yValues)
plt.plot([xValues[0], xValues[len(xValues)-1]], [m * xValues[0] + b, m * xValues[len(xValues)-1] + b] )
plt.show()
print "The most probable value of y at x = 3.5 is : ", 3.5 * m + b, " with an uncertainty of :", sigma(xValues, yValues, m, b)
printResiduals(xValues, yValues, m, b)


#this is the scatter plot with the line of best fit for
xValues = np.array([1.1, 1.6, 2.0, 2.1, 2.9, 3.2,  4.4, 4.9])
yValues = np.array([72.61, 72.91, 73.00, 73.11, 73.52, 73.70, 74.26, 74.51])
plt.scatter(xValues, yValues )
m, b = bestFit(xValues, yValues)
plt.plot([xValues[0], xValues[len(xValues)-1]], [m * xValues[0] + b, m * xValues[len(xValues)-1] + b] )
plt.show()
printResiduals(xValues, yValues, m, b)
print sigma(xValues, yValues, m, b)
