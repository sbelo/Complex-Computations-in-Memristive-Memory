from MAGIC import MAGIC
import numpy as np
from functions import randrange_float
import matplotlib.pyplot as plt
import random as rand

##################################################
# running abs func
##################################################

# initiating simulation
N = rand.randint(5,15)
p = rand.randint(0,N-1)
myMAGIC = MAGIC()
myMAGIC.F_simulation_init(N,p)

in_arr = np.array([])
out_arr = np.array([])

lines = 1000
# writing some numbers to MAGIC. msb in 0 column
for i in range (0,lines):
    val = randrange_float(start=-(2**(N-p-1)),stop= (2**(N-p-1)) - (2**(-p)),step=2**(-p))
    in_arr = np.r_[in_arr,val]
    row_add = i
    msb_add = 0
    myMAGIC.F_write_num(row_add, msb_add, val)

rows = np.arange(0,len(myMAGIC))
myMAGIC.F_abs(rows, 0, N)

# reading the abs numbers from MAGIC. msb in 7 column
for i in range (0,len(myMAGIC)):
    row_add = i
    msb_add = N
    out_arr = np.r_[out_arr, myMAGIC.F_read_num(row_add, msb_add)]

# ending simulation with prints and graphs
myMAGIC.F_simulation_end()

print "in_arr = ",in_arr
print "out_arr = ",out_arr

plt.figure(2)
plt.plot(in_arr,out_arr, 'ro', ms=1)
plt.xlabel('inputs')
plt.ylabel('outputs')
plt.title('abs operation with N=%d, p=%d' %(N,p))
plt.show()
