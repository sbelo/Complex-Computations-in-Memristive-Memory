from MAGIC import MAGIC
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from functions import randrange_float

##################################################
# running DIV_approx function
##################################################

# initiating simulation
N_old = rand.randint(5,10)
p = rand.randint(3,N_old-2)
lines = 100
myMAGIC = MAGIC()
myMAGIC.F_simulation_init(N_old,p)
num_arr = np.array([])
div_arr = np.array([])
out_arr = np.array([])
exp_arr = np.array([])


# writing some numbers to MAGIC. msb in 0 column
for i in range (0,lines):
    val = randrange_float(start=-(2 ** (N_old - p - 1)) + 1, stop=(2 ** (N_old - p - 1)) - (2 ** (-p)), step=2 ** (-p))
    num_arr = np.r_[num_arr, val]
    row_add = i
    msb_add = 0
    myMAGIC.F_write_num(row_add, msb_add, val)

# writing second set of numbers to MAGIC. msb in N column
for i in range (0,len(myMAGIC)):
    val = randrange_float(start=-(2 ** (N_old - p - 1)), stop=(2 ** (N_old - p - 1)) - (2 ** (-p)), step=2 ** (-p))
    if val == 0: val +=1
    div_arr = np.r_[div_arr, val]
    row_add = i
    msb_add = N_old
    myMAGIC.F_write_num(row_add, msb_add, val)

# checking multiplication:
rows = np.arange(0,len(myMAGIC))
N_new = N_old +p #rand.randint(10,20)
p_new = p #rand.randint(0,N-1)
myMAGIC.F_2num_DIV_approx(rows, 0, N_old, 2*N_old, N=N_new, p=p_new)
for row in rows:
    exp_arr = np.r_[exp_arr, num_arr[row]/div_arr[row]]
    out_arr = np.r_[out_arr, myMAGIC.F_read_num(row, 2*N_old, n=N_new,p=p_new)]


# ending simulation with prints and graphs
myMAGIC.F_simulation_end()

print "num_arr = ",num_arr
print "div_arr = ",div_arr
print "out_arr = ",out_arr
print "exp_arr = ",exp_arr

plt.figure(2)
plt.plot(out_arr,exp_arr, 'bo', ms=1)
plt.xlabel('out results')
plt.ylabel('expected results')
plt.title('DIV_approx operation with N=%d, p=%d inputs. result N=%d, p=%d' %(N_old,p,N_new,p_new))
plt.show()