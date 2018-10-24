from visual import *
import orbit
import sex
import numpy as np
import make_ephem






my_lat = None
my_long = None





def get_chi_sq(jd_list, ra_list, dec_list, r, rdot, jd_r, latitude, longitude):
    chisq_ra = 0
    chisq_dec = 0
    for index, jd, in enumerate(jd_list):
        ra_gauss, dec_gauss = make_ephem.make_ephem(jd_r, jd_list[index], r, rdot, tau_step = .001, latitude =  latitude, longitude = longitude, )

        chisq_ra += (ra_list[index] * 15 - ra_gauss)**2
        chisq_dec += (dec_list[index] - dec_gauss)**2
    return chisq_ra, chisq_dec

def f_function(tau, r_guess):
    return 1 - (tau**2)/(2 * (r_guess**3))
def g_function(tau, r_guess):
    return tau - (tau**3)/(6 * (r_guess**3))
def get_a_1(f1, f3, g1, g3):
    return (g3)/(f1*g3-f3*g1)
def get_a_3(f1, f3, g1, g3):
    return (-g1)/(f1*g3-f3*g1)
def get_rho_1(a1, a3, R1, R2, R3, rhohat1, rhohat2, rhohat3 ):
    numer = dot(cross(R1, rhohat2), rhohat3) * a1 - dot(cross(R2, rhohat2),rhohat3) + dot(cross(R3,rhohat2),rhohat3) * a3
    denom = dot(cross(rhohat1, rhohat2), rhohat3) * a1
    return numer/denom
def get_rho_2(a1, a3, R1, R2, R3, rhohat1, rhohat2, rhohat3 ):
    numer = dot(cross(rhohat1, R1), rhohat3) * a1 - dot(cross(rhohat1, R2),rhohat3) + dot(cross(rhohat1,R3),rhohat3) * a3
    denom = dot(cross(rhohat1, rhohat2), rhohat3) * -1
    return numer/denom
def get_rho_3(a1, a3, R1, R2, R3, rhohat1, rhohat2, rhohat3 ):
    numer = dot(cross(rhohat2, R1), rhohat1) * a1 - dot(cross(rhohat2, R2),rhohat1) + dot(cross(rhohat2,R3),rhohat1) * a3
    denom = dot(cross(rhohat2, rhohat3), rhohat1) * a3
    return numer/denom


my_r_guess = 1.5
rdot_2 = vector(.7,.7,-.5)

Time =[2457948.86380, 2457952.64330, 2457964.67207]

RA =   [20.264375000022223, 20.32464722222222, 20.483430555522222]
Dec =   [28.94747222222222, 25.97886111112222, 15.029416666622224]
"""
t1 = jd[pre]
t2 = jd[mid]
t3 = jd[post]

tau1 = orbit.k * (t1-t2)
tau3 = orbit.k * (t3-t2)

rho_hat1 = vector(orbit.toXYZ(ra[pre], dec[pre]))
rho_hat2 = vector(orbit.toXYZ(ra[mid], dec[mid]))
rho_hat3 = vector(orbit.toXYZ(ra[post], dec[post]))
"""
t1 = Time[0]
t2 = Time[1]
t3 = Time[2]

tau1 = orbit.k * (t1-t2)
tau3 = orbit.k * (t3-t2)

rho_hat1 = vector(orbit.toXYZ(RA[0], Dec[0]))
rho_hat2 = vector(orbit.toXYZ(RA[1], Dec[1]))
rho_hat3 = vector(orbit.toXYZ(RA[2], Dec[2]))

R_1 = vector(orbit.ephem.position(t1, 10, 2))
R_2 = vector(orbit.ephem.position(t2, 10, 2))
R_3 = vector(orbit.ephem.position(t3, 10, 2))

for i in range(1):
    #do speed of light correction after first iteration:

    f_1 = f_function(tau1, my_r_guess)
    f_3 = f_function(tau3, my_r_guess)
    g_1 = g_function(tau1, my_r_guess)
    g_3 = g_function(tau3, my_r_guess)

    a_1 = get_a_1(f_1, f_3, g_1, g_3)
    a_3 = get_a_3(f_1, f_3, g_1, g_3)

    rho_1 = get_rho_1(a_1, a_3, R_1, R_2, R_3, rho_hat1, rho_hat2, rho_hat3)
    rho_2 = get_rho_2(a_1, a_3, R_1, R_2, R_3, rho_hat1, rho_hat2, rho_hat3)
    rho_3 = get_rho_3(a_1, a_3, R_1, R_2, R_3, rho_hat1, rho_hat2, rho_hat3)

    r_2 = rho_2 * rho_hat2 - R_2
    r_1 = rho_1 * rho_hat1 - R_1
    r_3 = rho_3 * rho_hat3 - R_3

    my_r_guess = mag(r_2)
    rdot_2 = (f_3 * r_1)/(g_1 * f_3 - g_3 * f_1) - (f_1 * r_3)/(g_1 * f_3 - g_3 * f_1)


#speed of light correction occurs after the first loop
t1 = t1 - rho_1/orbit.c
t2 = t2 - rho_2/orbit.c
t3 = t3 - rho_3/orbit.c

tau1 = orbit.k * (t1-t2)
tau3 = orbit.k * (t3-t2)

R_1 = vector(orbit.ephem.position(t1, 10, 2))
R_2 = vector(orbit.ephem.position(t2, 10, 2))
R_3 = vector(orbit.ephem.position(t3, 10, 2))

for i in range(10):
    #do speed of light correction after first iteration:

    f_1 = f_function(tau1, my_r_guess)
    f_3 = f_function(tau3, my_r_guess)
    g_1 = g_function(tau1, my_r_guess)
    g_3 = g_function(tau3, my_r_guess)

    a_1 = get_a_1(f_1, f_3, g_1, g_3)
    a_3 = get_a_3(f_1, f_3, g_1, g_3)

    rho_1 = get_rho_1(a_1, a_3, R_1, R_2, R_3, rho_hat1, rho_hat2, rho_hat3)
    rho_2 = get_rho_2(a_1, a_3, R_1, R_2, R_3, rho_hat1, rho_hat2, rho_hat3)
    rho_3 = get_rho_3(a_1, a_3, R_1, R_2, R_3, rho_hat1, rho_hat2, rho_hat3)

    r_2 = rho_2 * rho_hat2 - R_2
    r_1 = rho_1 * rho_hat1 - R_1
    r_3 = rho_3 * rho_hat3 - R_3

    my_r_guess = mag(r_2)
    rdot_2 = (f_3 * r_1)/(g_1 * f_3 - g_3 * f_1) - (f_1 * r_3)/(g_1 * f_3 - g_3 * f_1)



#gives r and rdot for the middle observation
print "r_2: ", r_2
print "rdot_2", rdot_2
#print "time_2", jd[mid]

#print orbit.getOrbital(r_2, rdot_2)


"""
for index, day in enumerate(jd):
    rafound, decfound =  make_ephem.make_ephem(jd[mid], jd[index], r_2, rdot_2, tau_step =.001, latitude = my_lat, longitude = my_long)
    print "RA_model, Dec_model, RA, Dec, jd, resids:", rafound/15., decfound, ra[index], dec[index], day, ra[index] - rafound/15, dec[index] - decfound

print "Chisq_ra, chisq_dec:", get_chi_sq(jd, ra, dec, r_2, rdot_2, jd[mid], my_lat, my_long)
"""
orbit.getOrbital(r_2, rdot_2)
