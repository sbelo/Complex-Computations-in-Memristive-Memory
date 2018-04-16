from MAGIC import MAGIC
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from functions import randrange_float

##################################################
# running MUL function
##################################################

# initiating simulation
N = rand.randint(10,20)
p = rand.randint(0,N-1)
lines = 100
myMAGIC = MAGIC()
myMAGIC.F_simulation_init(N,p)
in1_arr = np.array([])
in2_arr = np.array([])
out_arr = np.array([])
exp_arr = np.array([])

# writing some numbers to MAGIC. msb in 0 column
for i in range (0,lines):
    val = randrange_float(start=-(2 ** ((N-p - 1)/2))+1, stop=(2 ** ((N-p - 1)/2))-1, step=(2 ** (-p/2)))
    in1_arr = np.r_[in1_arr, val]
    row_add = i
    msb_add = 0
    myMAGIC.F_write_num(row_add, msb_add, val)

# writing second set of numbers to MAGIC. msb in N column
for i in range (0,len(myMAGIC)):
    val = randrange_float(start=-(2 ** ((N-p - 1)/2))+1, stop=(2 ** ((N-p - 1)/2))-1, step=(2 ** (-p/2)))
    in2_arr = np.r_[in2_arr, val]
    row_add = i
    msb_add = N
    myMAGIC.F_write_num(row_add, msb_add, val)

# checking multiplication:
rows = np.arange(0,len(myMAGIC))
myMAGIC.F_2num_MUL(rows, 0, N, 2*N)
for row in rows:
    exp_arr = np.r_[exp_arr, in1_arr[row] * in2_arr[row]]
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
plt.title('MUL operation with N=%d, p=%d' %(N,p))
plt.show()