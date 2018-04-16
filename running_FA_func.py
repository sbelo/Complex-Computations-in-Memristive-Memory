from MAGIC import MAGIC
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from functions import randrange_float

##################################################
# running FA functions
##################################################

# initiating simulation
N = 8#rand.randint(10,20)
p = 0#rand.randint(0,N-1)

myMAGIC = MAGIC()
myMAGIC.F_simulation_init(N,p)
in1_arr = np.array([])
in2_arr = np.array([])
out_arr = np.array([])
exp_arr = np.array([])

lines = 1
# writing some numbers to MAGIC. msb in 0 column
for i in range (0,lines):
    val = randrange_float(start=-(2 ** (N - p - 2)), stop=(2 ** (N - p - 2)) - (2 ** (-p)), step=2 ** (-p))
    in1_arr = np.r_[in1_arr, val]
    row_add = i
    msb_add = 0
    myMAGIC.F_write_num(row_add, msb_add, -1)#val)

# writing second set of numbers to MAGIC. msb in N column
for i in range (0,len(myMAGIC)):
    val = randrange_float(start=-(2 ** (N - p - 2)), stop=(2 ** (N - p - 2)) - (2 ** (-p)), step=2 ** (-p))
    in2_arr = np.r_[in2_arr, val]
    row_add = i
    msb_add = N
    myMAGIC.F_write_num(row_add, msb_add, -1)#val)

# checking full adder on 2 bits with & without carry in
rows = np.arange(0,len(myMAGIC))
myMAGIC.F_2num_FA(rows, 0, N, 2*N, carry_in =0,carry_out_add=3*N)
for row in rows:
    exp_arr = np.r_[exp_arr, in1_arr[row] + in2_arr[row]]
    out_arr = np.r_[out_arr, myMAGIC.F_read_num(row,2*N)]

# ending simulation with prints and graphs
myMAGIC.F_simulation_end()

print "in1_arr = ",in1_arr
print "in2_arr = ",in2_arr
print "out_arr = ",out_arr
print "exp_arr = ",exp_arr

plt.figure(2)
plt.plot(out_arr,exp_arr, 'bo', ms=1)
plt.xlabel('out results')
plt.ylabel('expected results')
plt.title('FA operation with N=%d, p=%d' %(N,p))
plt.show()