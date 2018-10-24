import matplotlib.pyplot as plt
import numpy as np
import math





def exp_taylor(x, order = 100, center = 0):
    if order == 0:
        return 1
    return ((x-center)**order)/float((math.factorial(order))) + exp_taylor(x, order - 1)


def sin_taylor(x, order = 100):
    if order == 0:
        return 0
    elif order == 1:
        return x
    elif order % 2 == 0:
        return sin_taylor(x, order - 1)
    else:
        return  (-1 ** ((order - 1) / 2)) * (1/float(math.factorial(order))) * (x ** order) + sin_taylor(x, order - 1)




plt.style.use('seaborn-white')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'


x = np.linspace(-1, 5, num = 100)


plt.subplot(2,1,1)

plt.plot (x, np.exp(x), '', label = "Numpy Function")
plt.plot (x, exp_taylor(x, 1), '', label = "1st order Taylor")
plt.plot (x, exp_taylor(x, 3), '', label = "3rd order Taylor" )
plt.plot (x, exp_taylor(x, 6), '', label = "6th order Taylor" )
plt.plot (x, exp_taylor(x, 12), '', label = "12th order Taylor")
plt.title("Exponential Function")
plt.xlabel("x")
plt.ylabel("$e^x$")
plt.legend(loc = "best")

plt.subplot(2,1,2)

plt.plot (x, np.exp(x) - exp_taylor(x, 1), '', label = "1st order Taylor")
plt.plot (x, np.exp(x) - exp_taylor(x, 3), '', label = "3rd order Taylor" )
plt.plot (x, np.exp(x) - exp_taylor(x, 6), '', label = "6th order Taylor" )
plt.plot (x, np.exp(x) - exp_taylor(x, 12), '', label = "12th order Taylor")
plt.title("Differences")
plt.xlabel("x")
plt.ylabel("$e^x$-x")
plt.legend(loc = "best")

'''
x = np.linspace(-2, 2, num = 100)

plt.plot (x, np.sin(x), '', label = "Numpy Function")
plt.plot (x, sin_taylor(x, 1), '', label = "1st order Taylor")
plt.plot (x, sin_taylor(x, 3), '', label = "3rd order Taylor" )
plt.plot (x, sin_taylor(x, 6), '', label = "6th order Taylor" )
plt.plot (x, sin_taylor(x, 12), '', label = "12th order Taylor")
plt.title("Sin Function")
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.legend(loc = "best")
'''

plt.show()
