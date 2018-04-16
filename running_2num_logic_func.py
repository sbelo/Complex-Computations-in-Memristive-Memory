from MAGIC import MAGIC
import numpy as np
from functions import randrange_float
import matplotlib.pyplot as plt
import random as rand

##################################################
# running 2num logic functions
##################################################

# initiating simulation
N = rand.randint(1,10)
p = rand.randint(0,N-1)
myMAGIC = MAGIC()
myMAGIC.F_simulation_init(N,p)

lines = 1000
# writing some numbers to MAGIC. msb in 0 column
for i in range (0,lines):
    val = i #randrange_float(start=-(2**(N-p-1)),stop= (2**(N-p-1)) - (2**(-p)),step=2**(-p))
    row_add = i
    msb_add = 0
    myMAGIC.F_write_num(row_add, msb_add, val)

# writing some numbers to MAGIC. msb in Nth column
for i in range (0,lines):
    val = randrange_float(start=-(2**(N-p-1)),stop= (2**(N-p-1)) - (2**(-p)),step=2**(-p))
    row_add = i
    msb_add = N
    myMAGIC.F_write_num(row_add, msb_add, val)


# running 2num logic functions in parallel
rows = np.arange(0,len(myMAGIC))

myMAGIC.F_2num_XOR(rows, 0, N, 2*N)
myMAGIC.F_2num_NOR(rows, 0, N, 3*N)
myMAGIC.F_2num_AND(rows, 0, N, 4*N)
myMAGIC.F_2num_OR (rows, 0, N, 5*N)
myMAGIC.F_1num_NOT(rows, 0, 6*N)

# ending simulation with prints and graphs
myMAGIC.F_simulation_end()
plt.show()