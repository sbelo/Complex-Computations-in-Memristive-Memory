
from MAGIC_CMPLX import MAGIC_CMPLX
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from functions import (randrange_float, print_equation)



N = 32
p = 0
N_Array = range(1,N+1)
end_mem_arr = np.array([])
max_mem_arr = np.array([])
cycles_arr = np.array([])
for n in range(1, N+1):
    myMAGIC = MAGIC_CMPLX()
    myMAGIC.F_simulation_init(n,p,print_=0)

    for i in range(2):
        Real = randrange_float(start=-(2 ** ((N / 2 - p / 2 - 1) / 2)) + 1, stop=(2 ** ((N / 2 - p / 2 - 1) / 2)) - 1, step=(2 ** (-p / 4)))
        Imaginary = randrange_float(start=-(2 ** ((N / 2 - p / 2 - 1) / 2)) + 1, stop=(2 ** ((N / 2 - p / 2 - 1) / 2)) - 1, step=(2 ** (-p / 4)))
        myMAGIC.F_write_CMPLX_num(0, i*2*n, [Real,Imaginary])

    rows = np.arange(0,len(myMAGIC))

    #################################################################
    # choose a function by deleting the '#' from the wanted function
    # *** change the graph names accordingly
    #################################################################

    #myMAGIC.F_2num_MUL(rows, in1_msb=0, in2_msb=2 * n, out_add=4 * n)
    myMAGIC.F_2num_DIV_remain(rows, numerator_add=0, divisor_add=2 * n, out_add=4 * n, remain_add=6 * n)
    #myMAGIC.F_2num_DIV_approx(rows, numerator_add=0, divisor_add=2 * n, out_add=4 * n)
    #myMAGIC.F_2num_FA(rows, in1_msb=0, in2_msb=2 * n, out_add=4 * n)

    #################################################################

    [total_cycles, memory_at_the_end, max_memory] = myMAGIC.F_simulation_end(print_=0)
    cycles_arr = np.r_[cycles_arr, total_cycles]
    end_mem_arr = np.r_[end_mem_arr, memory_at_the_end]
    max_mem_arr = np.r_[max_mem_arr, max_memory]

Cycles_func = np.polyfit(N_Array,cycles_arr,2)

print "time complexity as a function of N:"
print_equation(Cycles_func,'N')
print Cycles_func
max_Mem_func = np.polyfit(N_Array,max_mem_arr,1)

print "memristor use as a function of N:"
print_equation(max_Mem_func,'N')
print max_Mem_func

xp = np.linspace(0,32,100)
Cycles_plt = np.poly1d(Cycles_func)
max_Mem_plt = np.poly1d(max_Mem_func)

# plt.figure(1)
# plt.plot(N_Array,max_mem_arr, 'bo', xp, max_Mem_plt(xp), '-', ms=1)
# plt.xlabel('N')
# plt.ylabel('max memristor use')
# plt.title('memristor use in CMPLX_MUL operation')
#
# plt.figure(2)
# plt.plot(N_Array,end_mem_arr, 'bo', ms=1)
# plt.xlabel('N')
# plt.ylabel('memristor use in the end of operation')
# plt.title('memristor use in CMPLX_MUL operation')
#
# plt.figure(3)
# plt.plot(N_Array,cycles_arr, 'bo', xp, Cycles_plt(xp), '-', ms=1)
# plt.xlabel('N')
# plt.ylabel('cycles')
# plt.title('cycles in CMPLX_MUL operation')


plt.figure(1)
plt.plot(N_Array,max_mem_arr, 'bo', xp, max_Mem_plt(xp), '-', ms=1)
plt.xlabel('N')
plt.ylabel('max memristor use')
plt.title('memristor use in CMPLX_DIV_remain operation')

plt.figure(2)
plt.plot(N_Array,end_mem_arr, 'bo', ms=1)
plt.xlabel('N')
plt.ylabel('memristor use in the end of operation')
plt.title('memristor use in CMPLX_DIV_remain operation')

plt.figure(3)
plt.plot(N_Array,cycles_arr, 'bo', xp, Cycles_plt(xp), '-', ms=1)
plt.xlabel('N')
plt.ylabel('cycles')
plt.title('cycles in CMPLX_DIV_remain operation')

# plt.figure(1)
# plt.plot(N_Array,max_mem_arr, 'bo', xp, max_Mem_plt(xp), '-', ms=1)
# plt.xlabel('N')
# plt.ylabel('max memristor use')
# plt.title('memristor use in CMPLX_FA operation')
#
# plt.figure(2)
# plt.plot(N_Array,end_mem_arr, 'bo', ms=1)
# plt.xlabel('N')
# plt.ylabel('memristor use in the end of operation')
# plt.title('memristor use in CMPLX_FA operation')
#
# plt.figure(3)
# plt.plot(N_Array,cycles_arr, 'bo', xp, Cycles_plt(xp), '-', ms=1)
# plt.xlabel('N')
# plt.ylabel('cycles')
# plt.title('cycles in CMPLX_FA operation')

plt.show()