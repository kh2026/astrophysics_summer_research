def toRADec(v):
    #finds the RA in hr using the x and y coordinates
    if v.x == 0:
        if v.y > 0:
            RA = math.pi / 2
        else:
            RA = 3 * math.pi/2
    else:
        RA = np.arctan(v.y/v.x)
    #adds pi rad if x<0 because arctan can only give between -pi/2 and pi/2
    if (v.x < 0):
        RA += math.pi
    #convert to degrees and make sure is positive
    RA = math.degrees(RA)/15.

    if(RA<0):
        RA += 360

    #finds the dec based on the ratio of the z coordinate and the planar length
    if (v.z == 1):
        Dec = math.pi/2
    else:
        Dec = np.arctan(v.z/math.sqrt(v.x * v.x + v.y * v.y))
    if (Dec < 0):
        Dec += 2 * math.pi
    Dec = math.degrees(Dec)

    return RA, Dec
