from visual import *
import orbit
import sex
import numpy as np
import make_ephem
import time
from decimal import Decimal
start = time.time()



def get_chi_sq(jd_list, ra_list, dec_list, r, rdot, jd_r, latitude, longitude):
    chisq_ra = 0
    chisq_dec = 0
    for index, jd, in enumerate(jd_list):
        ra_gauss, dec_gauss = make_ephem.make_ephem(jd_r, jd_list[index], r, rdot, tau_step = .001, latitude =  latitude, longitude = longitude, )

        chisq_ra += (ra_list[index] * 15 - ra_gauss)**2
        chisq_dec += (dec_list[index] - dec_gauss)**2
    return "chisq", chisq_ra, chisq_dec

def gradient_climb(jd_list, ra_list, dec_list, r_initial, rdot_initial, jd_r, latitude, longitude):
    #initial params
    best_chisq = get_chi_sq(jd_list, ra_list, dec_list, r_initial, rdot_initial, jd_r, latitude, longitude)
    step_size = .0001
    count = 0
    r = r_initial
    rdot = rdot_initial
    while time.time() - start <= 1800:
        test_r_x =np.random.normal(r.x, step_size)
        test_r_y =np.random.normal(r.y, step_size)
        test_r_z =np.random.normal(r.z, step_size)
        test_rdot_x =np.random.normal(rdot.x, step_size)
        test_rdot_y =np.random.normal(rdot.y, step_size)
        test_rdot_z =np.random.normal(rdot.z, step_size)
        test_r = vector(test_r_x, test_r_y, test_r_z)
        test_rdot = vector(test_rdot_x, test_rdot_y, test_rdot_z)

        test_chisq = get_chi_sq(jd_list, ra_list, dec_list, test_r, test_rdot, jd_r, latitude, longitude)
        print test_r, test_rdot
        if test_chisq < best_chisq:
            best_chisq = test_chisq
            r = vector(test_r_x, test_r_y, test_r_z)
            rdot =vector(test_rdot_x, test_rdot_y, test_rdot_z)
            count = 0
        else:
            count += 1

        if count > 1000:
            step_size /= 10.
            count = 0
        print "run", count, test_chisq

    print "r, rdot:"
    for dim in r:
        print str(Decimal.from_float(dim))
    for dim in rdot:
        print str(Decimal.from_float(dim))
    print "smallest chisq:", best_chisq


















my_lat = 41.3083
my_long = -72.9279


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


r = vector( 0.63688345, -1.03920149, -0.23511263)
rdot = vector( 0.92668992,  0.44938058, -0.09870414)
mid = 15

'''
0.613964406392347061824921183870173990726470947265625
-1.096588119112344994476870851940475404262542724609375
-0.2116846217022806675434054568540886975824832916259765625
0.9654570615788011789248912464245222508907318115234375
0.40112353261377176050217485681059770286083221435546875
-0.12767850918550693872788315275101922452449798583984375
smallest chisq: 3.24446506629
'''

print "r:", r, "rdot:", rdot, "r_time", jd[mid]
for index, day in enumerate(jd):
    rafound, decfound =  make_ephem.make_ephem(jd[mid], jd[index], r, rdot, tau_step =.001, latitude = my_lat, longitude = my_long)
    print rafound/15., decfound, ra[index], dec[index], day, ra[index] - rafound/15, dec[index] - decfound

print "rachisq, decchisq", get_chi_sq(jd, ra, dec, r, rdot, jd[13], latitude = my_lat, longitude = my_long)
orbit.getOrbital(r, rdot)
'''
gradient_climb(jd, ra, dec, r, rdot, jd[13], latitude = my_lat, longitude = my_long)
'''
