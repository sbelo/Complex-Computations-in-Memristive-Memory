from MAGIC_CMPLX import MAGIC_CMPLX
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from functions import randrange_float

##################################################
# running FA function
##################################################

# initiating simulation
N = rand.randint(10,20)
p = rand.randint(0,N-1)

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
lines = 1000
# writing some numbers to MAGIC. msb in 0 column
for i in range (0,lines):
    Real = randrange_float(start=-(2 ** (N - p - 2)), stop=(2 ** (N - p - 2)) - (2 ** (-p)), step=2 ** (-p))
    Imaginary = randrange_float(start=-(2 ** (N - p - 2)), stop=(2 ** (N - p - 2)) - (2 ** (-p)), step=2 ** (-p))
    in1_arr_Re = np.r_[in1_arr_Re, Real]
    in1_arr_Im = np.r_[in1_arr_Im, Imaginary]
    row_add = i
    msb_add = 0
    myMAGIC.F_write_CMPLX_num(row_add, msb_add, [Real,Imaginary])

# writing second set of numbers to MAGIC. msb in N column
for i in range (0,len(myMAGIC)):
    Real = randrange_float(start=-(2 ** (N - p - 2)), stop=(2 ** (N - p - 2)) - (2 ** (-p)), step=2 ** (-p))
    Imaginary = randrange_float(start=-(2 ** (N - p - 2)), stop=(2 ** (N - p - 2)) - (2 ** (-p)), step=2 ** (-p))
    in2_arr_Re = np.r_[in2_arr_Re, Real]
    in2_arr_Im = np.r_[in2_arr_Im, Imaginary]
    row_add = i
    msb_add = 2*N
    myMAGIC.F_write_CMPLX_num(row_add, msb_add, [Real,Imaginary])

# checking full adder on 2 bits with & without carry in
rows = np.arange(0,len(myMAGIC))
myMAGIC.F_2num_FA(rows, in1_msb=0, in2_msb=2*N, out_add=4*N)
for row in rows:
    exp_arr_Re = np.r_[exp_arr_Re, in1_arr_Re[row] + in2_arr_Re[row]]
    exp_arr_Im = np.r_[exp_arr_Im, in1_arr_Im[row] + in2_arr_Im[row]]
    result = myMAGIC.F_read_num(row_address=row, msb_address=4*N)
    out_arr_Re = np.r_[out_arr_Re, result[0]]
    out_arr_Im = np.r_[out_arr_Im, result[1]]

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
plt.title('REAL FA operation with N=%d, p=%d' %(N,p))

plt.figure(3)
plt.plot(out_arr_Im,exp_arr_Im, 'bo', ms=1)
plt.xlabel('out results')
plt.ylabel('expected results')
plt.title('IMAGINARY FA operation with N=%d, p=%d' %(N,p))

plt.show()