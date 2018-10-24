#conversions from base 10 to base 60 and back

def toHMS(deg):
    deg /= 15.0

    if (deg < 0):
        deg *= -1

        h = int(deg)
        deg = 60 * (deg % 1)
        m = int(deg)

        deg = 60 * (deg % 1)
        s = deg

        return -h, -m, -s
    else:

        h = int(deg)
        deg = 60 * (deg % 1)
        m = int(deg)

        deg = 60 * (deg % 1)
        s = deg

        return h, m, s

def formatHMS(deg):
    h, m, s = toHMS(deg)
    return str(h) + " hours, " + str(m) + " minutes, " + str(s) + " seconds"


def toDMS(x):

        if (x < 0):
            x *= -1

            d = int(x)
            x = 60 * (x % 1)
            m = int(x)

            x = 60 * (x % 1)
            s = x

            return -d, -m, -s
        else:

            d = int(x)
            x = 60 * (x % 1)

            m = int(x)

            x = 60 * (x % 1)
            s = x

            return d, m, s

def formatDMS(deg):
    d, m, s = toDMS(deg)
    return str(d) + " degrees, " + str(m) + " minutes, " + str(s) + " seconds"

def to10(d, m, s):
    return d + m/60.0 + s/3600.0
