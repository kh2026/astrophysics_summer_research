import numpy as np
import sex

#modify these parameters
fileName = "/home/student/python/data/exampleLSPR.txt"
astX = 357.62
astY = 324.02



#RA (in deg), Dec (in deg), x, y should be the 4 columns of the file
RA, Dec, x, y = np.loadtxt(fileName,   delimiter = ", ", dtype = float, unpack = True)

#this part finds the least squares solutions for RA and Dec
bigArr = np.matrix([
[len(RA), sum(x), sum(y)],
[sum(x),sum(x*x), sum(x*y)],
[sum(y),sum(x*y), sum(y*y)]
])

RAVec = np.matrix([[sum(RA)],[sum(RA*x)],[sum(RA*y)]])
DecVec = np.matrix([[sum(Dec)],[sum(Dec*x)],[sum(Dec*y)]])

#RA = b_1 + a_11 * x + a_12 * y, b_1 is row 0, a_11 is row 1, a_12 is row 2
#RASol is a vector
RASol = np.linalg.solve(bigArr, RAVec)
#Dec = b_2 + a_21 * x + a_22 * y, b_2 is row 0, a_21 is row 1, a_22 is row 2
#DecSol is a vector
DecSol = np.linalg.solve(bigArr, DecVec)


#prints the RA and Dec
print "RA = ", float(RASol[0]), " + ", float(RASol[1]), " * x + ", float(RASol[2]), " * y"
print "Dec = ", float(DecSol[0]), " + ", float(DecSol[1]), " * x + ", float(DecSol[2]), " * y"


#this creates two arrays with the residuals
RAResid = RA - (float(RASol[0]) + float(RASol[1]) * x + float(RASol[2]) * y)
DecResid = Dec - (float(DecSol[0]) + float(DecSol[1]) * x + float(DecSol[2]) * y)

#outputs the list of residuals
print "Residuals:"
for i in range(len(RA)):
    print "Star #", i+1, "\tRA = ", RAResid[i], "\t Dec = ", DecResid[i]

#print the standard deviation of the residuals
print "Sigma(RA) = ", np.std(RAResid), "\tSigma(Dec) = ", np.std(DecResid)

#print the expected coordinates of the asteroid
print "The asteroid's expected coordinates are: \nRA = ", sex.formatHMS((float(RASol[0]) + float(RASol[1]) * astX + float(RASol[2]) * astY)),  \
"\nDec = ", sex.formatDMS((float(DecSol[0]) + float(DecSol[1]) * astX + float(DecSol[2]) * astY))
