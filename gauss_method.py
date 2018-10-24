from visual import *
import orbit
import sex
import numpy as np
import make_ephem



'''
my_lat = 41.3083
my_long = -72.9279


f = open("/home/student/python/data/sample_gauss.csv")

jd, ra, dec, lum = [], [], [], []

#data
for line in f.readlines():
    d_1, d_2, d_3, d_4, d_5, d_6, d_7, d_8 =(line.split(", "))
    jd.append(float(d_1))
    ra.append(sex.to10(float(d_2), float(d_3), float(d_4)))
    dec.append(sex.to10(float(d_5), float(d_6), float(d_7)))
    lum.append(float(d_8))
for index, d in enumerate(dec):
    if d < 0:
        dec[index] = d + 360

#pre is index of first data point, mid is index of middle data point, post is index of end data point
pre = 0
mid = 2
post = 4
'''


my_lat = None
my_long = None


f = open("/home/student/python/data/2002tx68format.csv")

jd, ra, dec, lum = [], [], [], []

#data
for line in f.readlines():
    d_1, d_2, d_3, d_4, d_5, d_6, d_7, d_8, d_9 =(line.split(", "))
    jd.append(float(d_1))
    ra.append(sex.to10(float(d_2), float(d_3), float(d_4)))
    dec.append(sex.to10(float(d_5), float(d_6), float(d_7)))
    lum.append(float(d_8))
for index, d in enumerate(dec):
    if d < 0:
        dec[index] = d + 360

#pre is index of first data point, mid is index of middle data point, post is index of end data point
pre = 1
mid = 15
post = 29

print "jd1, jd2, jd3", jd[pre], jd[mid], jd[post]

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

t1 = jd[pre]
t2 = jd[mid]
t3 = jd[post]

tau1 = orbit.k * (t1-t2)
tau3 = orbit.k * (t3-t2)

rho_hat1 = vector(orbit.toXYZ(ra[pre], dec[pre]))
rho_hat2 = vector(orbit.toXYZ(ra[mid], dec[mid]))
rho_hat3 = vector(orbit.toXYZ(ra[post], dec[post]))

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
print "time_2", jd[mid]

#print orbit.getOrbital(r_2, rdot_2)



for index, day in enumerate(jd):
    rafound, decfound =  make_ephem.make_ephem(jd[mid], jd[index], r_2, rdot_2, tau_step =.001, latitude = my_lat, longitude = my_long)
    print "RA_model, Dec_model, RA, Dec, jd, resids:", rafound/15., decfound, ra[index], dec[index], day, ra[index] - rafound/15, dec[index] - decfound

print "Chisq_ra, chisq_dec:", get_chi_sq(jd, ra, dec, r_2, rdot_2, jd[mid], my_lat, my_long)
orbit.getOrbital(r_2, rdot_2)
