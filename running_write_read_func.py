from MAGIC import MAGIC
import numpy as np
from functions import randrange_float
import matplotlib.pyplot as plt
import random as rand

##################################################
# running write and read functions
##################################################

# initiating simulation
N = rand.randint(1,10)
p = rand.randint(0,N-1)
myMAGIC = MAGIC()
myMAGIC.F_simulation_init(N,p)

in_arr = np.array([])
out_arr = np.array([])

# writing some numbers to MAGIC. msb in 0 column
for i in range (0,1000):
    val = randrange_float(start=-(2 ** (N - p - 1)), stop=(2 ** (N - p - 1)) - (2 ** (-p)), step=2 ** (-p))
    in_arr = np.r_[in_arr, val]
    row_add = i
    msb_add = 0
    myMAGIC.F_write_num(row_add, msb_add, val)

# writing some numbers to MAGIC. msb in Nth column
for i in range (0,1000):
    val = randrange_float(start=-(2 ** (N - p - 1)), stop=(2 ** (N - p - 1)) - (2 ** (-p)), step=2 ** (-p))
    row_add = i
    msb_add = N
    myMAGIC.F_write_num(row_add, msb_add, val)

# reading numbers from MAGIC. msb in 0 column
for i in range (0,len(myMAGIC)):
    row_add = i
    msb_add = 0
    out_arr = np.r_[out_arr, myMAGIC.F_read_num(row_add, msb_add)]

# ending simulation with prints and graphs
myMAGIC.F_simulation_end()


plt.figure(2)
plt.plot(in_arr,out_arr, 'ro', ms=1)
plt.show()