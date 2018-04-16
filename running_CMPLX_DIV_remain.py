from MAGIC_CMPLX import MAGIC_CMPLX
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from functions import randrange_float

##################################################
# running CMPLX_DIV_remain function
##################################################

# initiating simulation
N = 2*rand.randint(5,10)
p = 2*rand.randint(2,(N-1)/2-N/5)
myMAGIC = MAGIC_CMPLX()
myMAGIC.F_simulation_init(N,p)
in1_arr_Re = np.array([])
in1_arr_Im = np.array([])
in2_arr_Re = np.array([])
in2_arr_Im = np.array([])
out_arr_Re = np.array([])
out_arr_Im = np.array([])
exp_arr_Re = np.array([])
exp_arr_Im = np.array([])
lines = 20
# writing some numbers to MAGIC. msb in 0 column
for i in range (0,lines):
    Real = randrange_float(start=-(2 ** ((N/2-p/2 - 1)/2))+1, stop=(2 ** ((N/2-p/2 - 1)/2))-1, step=(2 ** (-p/4)))
    Imaginary = randrange_float(start=-(2 ** ((N/2-p/2 - 1)/2))+1, stop=(2 ** ((N/2-p/2 - 1)/2))-1, step=(2 ** (-p/4)))
    in1_arr_Re = np.r_[in1_arr_Re, Real]
    in1_arr_Im = np.r_[in1_arr_Im, Imaginary]
    row_add = i
    msb_add = 0
    myMAGIC.F_write_CMPLX_num(row_add, msb_add, [Real,Imaginary])

# writing second set of numbers to MAGIC. msb in N column
for i in range (0,len(myMAGIC)):
    Real = randrange_float(start=-(2 ** ((N/2-p/2 - 1)/2))+1, stop=(2 ** ((N/2-p/2 - 1)/2))-1, step=(2 ** (-p/4)))#randrange_float(start=-(2 ** ((N-p - 1)/2))+1, stop=(2 ** ((N-p - 1)/2))-1, step=(2 ** (-p/2)))
    Imaginary = randrange_float(start=-(2 ** ((N/2-p/2 - 1)/2))+1, stop=(2 ** ((N/2-p/2 - 1)/2))-1, step=(2 ** (-p/4)))#randrange_float(start=-(2 ** ((N-p - 1)/2))+1, stop=(2 ** ((N-p - 1)/2))-1, step=(2 ** (-p/2)))
    while (abs(Real) + abs(Imaginary) == 0):
        Real = randrange_float(start=-(2 ** ((N / 2 - p / 2 - 1) / 2)) + 1, stop=(2 ** ((N / 2 - p / 2 - 1) / 2)) - 1, step=(2 ** (-p / 4)))
        Imaginary = randrange_float(start=-(2 ** ((N / 2 - p / 2 - 1) / 2)) + 1, stop=(2 ** ((N / 2 - p / 2 - 1) / 2)) - 1, step=(2 ** (-p / 4)))

    in2_arr_Re = np.r_[in2_arr_Re, Real]
    in2_arr_Im = np.r_[in2_arr_Im, Imaginary]
    row_add = i
    msb_add = 2*N
    myMAGIC.F_write_CMPLX_num(row_add, msb_add, [Real,Imaginary])

# checking full adder on 2 bits with & without carry in
rows = np.arange(0,len(myMAGIC))

myMAGIC.F_2num_DIV_remain(rows, numerator_add=0, divisor_add=2*N, out_add=4*N, remain_add=6*N)
for row in rows:
    new_div = in2_arr_Re[row]*in2_arr_Re[row] + in2_arr_Im[row]*in2_arr_Im[row]
    new_num_Re = in1_arr_Re[row]*in2_arr_Re[row] + in1_arr_Im[row]*in2_arr_Im[row]
    new_num_Im =in1_arr_Im[row]*in2_arr_Re[row] - in1_arr_Re[row]*in2_arr_Im[row]
    exp_arr_Re = np.r_[exp_arr_Re, new_num_Re/new_div]
    exp_arr_Im = np.r_[exp_arr_Im, new_num_Im/new_div]
    result = myMAGIC.F_read_num(row_address=row, msb_address=4*N, p=0)
    remain = myMAGIC.F_read_num(row_address=row, msb_address=6*N)
    print "new_div = ", new_div
    print "result[0] = ", result[0]
    print "result[1] = ", result[1]
    print "remain[0] = ", remain[0]
    print "remain[1] = ", remain[1]
    out_arr_Re = np.r_[out_arr_Re, result[0] + remain[0]/new_div]
    out_arr_Im = np.r_[out_arr_Im, result[1] + remain[1]/new_div]

# ending simulation with prints and graphs
myMAGIC.F_simulation_end()

print "in1_arr_Re = ",in1_arr_Re
print "in1_arr_Im = ",in1_arr_Im
print "in2_arr_Re = ",in2_arr_Re
print "in2_arr_Im = ",in2_arr_Im
print "out_arr_Re = ",out_arr_Re
print "out_arr_Im = ",out_arr_Im
print "exp_arr_Re = ",exp_arr_Re
print "exp_arr_Im = ",exp_arr_Im

plt.figure(2)
plt.plot(out_arr_Re,exp_arr_Re, 'bo', ms=1)
plt.xlabel('out results')
plt.ylabel('expected results')
plt.title('REAL DIV_remain operation with N=%d, p=%d' %(N,p))

plt.figure(3)
plt.plot(out_arr_Im,exp_arr_Im, 'bo', ms=1)
plt.xlabel('out results')
plt.ylabel('expected results')
plt.title('IMAGINARY DIV_remain operation with N=%d, p=%d' %(N,p))

plt.show()