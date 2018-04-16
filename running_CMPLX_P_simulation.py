
from MAGIC_CMPLX import MAGIC_CMPLX
import numpy as np
import random as rand
import matplotlib.pyplot as plt
from functions import (randrange_float, print_equation)



N = 12
n=N
P_Array = range(0,N)
end_mem_arr = np.array([])
max_mem_arr = np.array([])
cycles_arr = np.array([])
for p in range(0,N):
    myMAGIC = MAGIC_CMPLX()
    myMAGIC.F_simulation_init(n,p,print_=0)

    for i in range(2):
        Real = randrange_float(start=-(2 ** ((N / 2 - p / 2 - 1) / 2)) + 1, stop=(2 ** ((N / 2 - p / 2 - 1) / 2)) - 1, step=(2 ** (-p / 4)))
        Imaginary = randrange_float(start=-(2 ** ((N / 2 - p / 2 - 1) / 2)) + 1, stop=(2 ** ((N / 2 - p / 2 - 1) / 2)) - 1, step=(2 ** (-p / 4)))
        myMAGIC.F_write_CMPLX_num(0, i*2*n, [Real,Imaginary])

    rows = np.arange(0,len(myMAGIC))
    myMAGIC.F_2num_DIV_approx(rows, numerator_add=0, divisor_add=2 * n, out_add=4 * n)

    [total_cycles, memory_at_the_end, max_memory] = myMAGIC.F_simulation_end(print_=0)
    cycles_arr = np.r_[cycles_arr, total_cycles]
    end_mem_arr = np.r_[end_mem_arr, memory_at_the_end]
    max_mem_arr = np.r_[max_mem_arr, max_memory]

Cycles_func = np.polyfit(P_Array,cycles_arr,2)
print "time complexity as a function of P:"
print_equation(Cycles_func,'P')
print Cycles_func

max_Mem_func = np.polyfit(P_Array,max_mem_arr,1)
print "memristor use as a function of P:"
print_equation(max_Mem_func,'P')
print max_Mem_func

xp = np.linspace(0,N,100)
Cycles_plt = np.poly1d(Cycles_func)
max_Mem_plt = np.poly1d(max_Mem_func)


plt.figure(1)
plt.plot(P_Array,max_mem_arr, 'bo', xp, max_Mem_plt(xp), '-', ms=1)
plt.xlabel('FIP')
plt.ylabel('max memristor use')
plt.title('memristor use in CMPLX_DIV_approx operation')

plt.figure(2)
plt.plot(P_Array,end_mem_arr, 'bo', ms=1)
plt.xlabel('FIP')
plt.ylabel('memristor use in the end of operation')
plt.title('memristor use in CMPLX_DIV_approx operation')

plt.figure(3)
plt.plot(P_Array,cycles_arr, 'bo', xp, Cycles_plt(xp), '-', ms=1)
plt.xlabel('FIP')
plt.ylabel('cycles')
plt.title('cycles in CMPLX_DIV_approx operation')

plt.show()