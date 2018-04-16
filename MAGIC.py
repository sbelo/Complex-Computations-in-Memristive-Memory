##################################################
#   file name: MAGIC
#   author: amnon wahle
#
#   description:
#   this file defines MAGIC class and all its functions.
#	MAGIC is basicly the memory array, implimented as list of memLines
##################################################
# TODO - seperate private from public functions & move global functions to "functions.py"
# TODO - add invert function

##################################################
#                   imports
##################################################
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from complexity_param import *
from mem_line import MemLine
from functions import dec2bin
from functions import bin2dec
# end of imports
##################################################

class MAGIC:
    # GLOBAL definitions, parameters etc. of MAGIC class

    # our MAGIC array
    MAGIC = []  # size of MAGIC array will be in define or parameter

    def __len__(self):
        return len(self.MAGIC)

    # global parameters
    N_bit = 7  # default numbers of bits representing each number
    FIP = 2  # defualt working resolution for fixed point representation

    # counters of all types and flavours
    C_mem     = 0
    C_mem_max = 0
    C_cycles  = 0

    # arrays to keep track of memristors use for later plot on graph
    mem_arr     = np.array([0])
    cycles_arr  = np.array([0])

    ##################################################
    # function name: F_simulation_init
    # inputs:
    #   N_bit - size of bits representing each number
    #   FIP - working resolution of fixed point (number of bits to the right of decimal point)
    # outputs:
    # description:
    #   initiating simulation: parameters, memory, counters
    def F_simulation_init(self, N_bit, FIP, print_=1):
        if print_ == 1:
            print "initating simulation"
            print "\tN_bit\t=\t", N_bit
            print "\tFIP\t\t=\t", FIP

        # initiating parameters of all types and flavours
        self.N_bit = N_bit
        self.FIP = FIP

        # initiating MAGIC array
        self.MAGIC = []  # size of MAGIC array will be in define or parameter

        # initiating counters of all types and flavours
        self.C_mem = 0
        self.C_cycles = 0
        self.mem_arr = np.array([0])
        self.cycles_arr = np.array([0])
    # end of function F_simulation_init
    ##################################################

    ##################################################
    # function name: F_simulation_end
    # inputs:
    # description:
    #   ending simulation with prints of all necessary prints and plot
    def F_simulation_end(self, print_=1):
        MAGIC.F_update_counters(self)
        if print_ == 1:
            print "\n"
            MAGIC.F_print(self)
            MAGIC.F_printCounters(self)
            print "simulation ended normaly"
            print "ploting graph..."
            MAGIC.F_mem_graph(self)
        return [self.C_cycles, self.C_mem, self.C_mem_max]
    # end of function F_simulation_end
    ##################################################

    ##################################################
    # function name: F_mem_graph
    # inputs:
    # description:
    #   ploting graph of memristor use as function of cycles
    def F_mem_graph(self):
        fig, graph = plt.subplots(1)

        graph.set_title('memristor use as function of cycles with N = %d, p = %d' %(self.N_bit,self.FIP))
        graph.plot(self.cycles_arr,self.mem_arr, label='memristors in use')
        graph.axhline(self.C_mem_max,color='r',linewidth=0.8,ls='--',label='maximum memristors use')
        #graph.axhline(self.C_mem_avg, color='g',linewidth=0.8,ls='--',label='average memristors use')
        graph.set_ylabel('number of memristors in use')
        graph.set_xlabel('number of cycles')
        graph.legend(loc='lower center')

    # end of function F_mem_graph
    ##################################################

    ##################################################
    # function name: F_print
    # inputs:
    # outputs:
    # description:
    #   printing MAGIC memory with all its content
    def F_print(self):
         print "MAGIC ="
         for i in range (0,len(self.MAGIC)):
            self.MAGIC[i].print_mem()
    # end of function F_print
    ##################################################

    ##################################################
    # function name: F_printCounters
    # inputs:
    # outputs:
    # description:
    #   printing all counters and their values to screen
    def F_printCounters(self):
        print "\nprinting couners:\n"
        print "\tC_mem\t\t=\t", self.C_mem
        print "\tC_cycles\t=\t", self.C_cycles
        print "\tC_mem_max\t=\t", self.C_mem_max
        print "\n\tmem_arr[]\t=\t", self.mem_arr
        print "\tcycles_arr[]=\t", self.cycles_arr
    # end of function F_printCounters
    ##################################################

    ##################################################
    # function name: F_update_counters
    # inputs:
    # outputs:
    # description:
    #   updating counters arrays
    def F_update_counters(self):
        # update C_mem according to current line length - use maximum length
        self.C_mem = len(self.MAGIC[0])

        # add last value of C_mem to mem_arr
        self.mem_arr    = np.r_[self.mem_arr, self.C_mem]

        # add last value of c_cycels to cycels_arr - assume C_cyce
        self.cycles_arr = np.r_[self.cycles_arr, self.C_cycles]
        self.C_mem_max = np.amax(self.mem_arr)
    # end of function F_update_counters
    ##################################################

    ##################################################
    # function name: F_write_num
    # inputs:
    #   row_address - the row address in memory where to write to
    #   msb_address - column address to write MSB input to
    #   value       - an array of the bits value to write into MAGIC
    #   n           - numbers of bits representing the number (default: class.N_bits)
    #   p           - numbers of bits representing the resolution of the number (default: class.FIP)
    # outputs:
    # description:
    #   writing a number into MAGIC array.
    #   input MSB & output MSB are given as inputs.
    #   N - size of bits representing the number is a parameter given.
    #   the function also updating counters accordingly.
    def F_write_num(self, row_address, msb_address, value, n = -1, p = -1):
        if n < 0: n = self.N_bit
        if p < 0: p = self.FIP
        bin_value = dec2bin(n, p, value)

        # make sure row is in bound
        if (row_address < 0):
            raise ValueError('cannot write into negative row number. row = %d' % (row_address))
        # assuming array is endless memory we allocate more lines in memory
        if (len(self.MAGIC)-1 < row_address):
            for i in range (len(self.MAGIC)-1,row_address):
                self.MAGIC.append(MemLine())
        # writing the numbers bit by bit
        for  i in range (0,len(bin_value)):
            MAGIC.__F_write_bit(self, row_address,msb_address + i,bin_value[i])
    # end of function F_write_num
    ##################################################

    ##################################################
    # function name: F_write_bit
    # inputs:
    #   row_address - the row address in memory where to write to
    #   bit_address - coloumn address to write MSB input to
    #   value - an array of the bits value to write into MAGIC
    # outputs:
    # description:
    #   writing a number into MAGIC array.
    def __F_write_bit(self,row_address,bit_address,value):

        # make sure row is in bound
        if (row_address < 0):
            raise ValueError('cannot write into negative row number. row = %d' % (row_address))
        if (len(self.MAGIC)-1 < row_address):
            for i in range (len(self.MAGIC)-1,row_address):
                self.MAGIC.append(MemLine())

        # make sure bit_address is not negative
        if (bit_address < 0):
            raise ValueError('cannot write into negative bit address. bit address = %d' %(bit_address))
        # writing is always poissible, if there is no space we allocate new space
        while (self.MAGIC[row_address].assign(bit_address,value) == -1) :
            self.MAGIC[row_address].allocate(1)
    # end of function F_write
    ##################################################

    ##################################################
    # function name: F_read_num
    # inputs:
    #   row_address - the row address in memory where to read from
    #   msb_address - the column address where the MSB to read from
    #   n           - numbers of bits representing the number (default: class.N_bits)
    #   p           - numbers of bits representing the resolution of the number (default: class.FIP)
    # outputs:
    #   reasult - a float number read from memory according to its address
    # description:
    #
    def F_read_num(self, row_address, msb_address, n = -1, p = -1):
           if n < 0: n = self.N_bit
           if p < 0: p = self.FIP

           # make sure row is in bound
           if (MAGIC.F_row_out_of_bound(self, row_address)):
              raise  ValueError('reading row out of bound. row = %d, while MAGIC has rows 0 to %d' %(row_address,len(self.MAGIC)-1))

           # make sure line is long enough
           row_length = len(self.MAGIC[row_address])
           if (msb_address < 0) or (msb_address + n - 1 > row_length):
               raise ValueError('reading outside row.\ntrying to read row[%d], bits %d to %d while row length is %d.' %(row_address,msb_address,msb_address+self.N_bit-1,row_length))

           vec = MemLine(n)
           for i in range (0 , n):
               vec[i] = self.MAGIC[row_address][msb_address + i]
           return bin2dec(p, vec)
    # end of function F_read
    ##################################################

    ##################################################
    # Function name: F_row_out_of_bound
    # inputs:
    #   row_address - the row address to check if in bound
    # outputs:
    #   result - 1 if out of bound, 0 if in bound
    # description:
    #   checking whether row is in bound
    def F_row_out_of_bound(self,row_address):
        if (row_address < 0) or (len(self.MAGIC) - 1 < row_address):
            return 1
        else:
            return 0
    # enf of function F_row_out_of_bound
    ##################################################

    ##################################################
    # Function name: F_mem_out_of_bound
    # inputs:
    #   row     - the row address to check if in bound
    #   mem_add - memristor address to check if in bound to that row
    # outputs:
    #   reasult - 1 if out of bound, 0 if in bound
    # description:
    #   checking whether memristor address is in bound
    def F_mem_out_of_bound(self, row, mem_add):
        if (mem_add < 0) or (len(self.MAGIC[row]) - 1 < mem_add):
            return 1
        else:
            return 0
    # enf of function F_mem_out_of_bound
    ##################################################

    ##################################################
    # function name: F_2num_NOR
    # inputs:
    #   rows - vector with row numbers to execute bit NOR on
    #   in1_msb  - address of first bit input
    #   in2_msb  - address of second bit input
    #   out_msb  - address of output bit
    #   n        - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   executing bit wise NOR on two inputs on all given rows.
    #   inputs are the addresses of msbs memristors to execute the operation on
    #   updates counters accordingly
    def F_2num_NOR(self, rows, in1_msb, in2_msb, out_add, n = -1):
        if n<0: n = self.N_bit
        rows = np.r_[rows]

        for row in rows:
            if (MAGIC.F_row_out_of_bound(self, row)):
                raise ValueError('trying to execute NOR on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (
                row, len(self.MAGIC) - 1))
            for i in range(0, n):
                if (MAGIC.F_mem_out_of_bound(self, row, in1_msb + i)) or (MAGIC.F_mem_out_of_bound(self, row, in2_msb + i)):
                    raise ValueError('trying to read memristor address outside row bound.')

                in1 = self.MAGIC[row][in1_msb + i]
                in2 = self.MAGIC[row][in2_msb + i]
                if (in1 + in2) == 0:     out = 1
                else:                    out = 0
                MAGIC.__F_write_bit(self, row, out_add + i, out)

        MAGIC.F_update_counters(self)
        self.C_cycles += 1 * n  # its takes 1 NOR iterations. initiation is done in calling function
        self.MAGIC[rows[0]].allocate(0)  # 0 mid results to save
        MAGIC.F_update_counters(self)
        self.MAGIC[rows[0]].free(0)
        MAGIC.F_update_counters(self)
    # end of function F_2num_NOR
    ##################################################

    ##################################################
    # function name: F_2num_OR
    # inputs:
    #   rows - vector with row numbers to execute bit OR on
    #   in1_msb  - address of first bit input
    #   in2_msb  - address of second bit input
    #   out_msb  - address of output bit
    #   n        - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   executing bit wise OR on two inputs on all given rows.
    #   inputs are the addresses of msbs memristors to execute the operation on
    #   updates counters accordingly
    def F_2num_OR(self, rows, in1_msb, in2_msb, out_add, n=-1):
        if n<0: n = self.N_bit
        rows = np.r_[rows]

        for row in rows:
            if (MAGIC.F_row_out_of_bound(self, row)):
                raise ValueError('trying to execute OR on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (
                row, len(self.MAGIC) - 1))
            for i in range(0, n):
                if (MAGIC.F_mem_out_of_bound(self, row, in1_msb + i)) or (MAGIC.F_mem_out_of_bound(self, row, in2_msb + i)):
                    raise ValueError('trying to read memristor address outside row bound.')

                in1 = self.MAGIC[row][in1_msb + i]
                in2 = self.MAGIC[row][in2_msb + i]
                if (in1 + in2) == 0:      out = 0
                else:                     out = 1
                MAGIC.__F_write_bit(self, row, out_add + i, out)

        MAGIC.F_update_counters(self)
        self.C_cycles += 2 * n  # its takes 2 NOR iterations. initiation is done in calling function
        self.MAGIC[rows[0]].allocate(1 * n)  # 1 mid results to save
        MAGIC.F_update_counters(self)
        self.MAGIC[rows[0]].free(1 * n)
        MAGIC.F_update_counters(self)
    # end of function F_2num_OR
    ##################################################

    ##################################################
    # function name: F_2num_XOR
    # inputs:
    #   rows - vector with row numbers to execute bit XOR on
    #   in1_msb  - address of first bit input
    #   in2_msb  - address of second bit input
    #   out_msb  - address of output bit
    #   n        - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   executing bit wise XOR on two inputs on all given rows.
    #   inputs are the addresses of msbs memristors to execute the operation on
    #   updating counters accordingly
    def F_2num_XOR(self, rows, in1_msb, in2_msb, out_add, n = -1):
        if n<0: n = self.N_bit
        rows = np.r_[rows]

        for row in rows:
            if (MAGIC.F_row_out_of_bound(self, row)):
                raise ValueError('trying to execute XOR on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (
                row, len(self.MAGIC) - 1))
            for i in range(0, n):
                if (MAGIC.F_mem_out_of_bound(self, row, in1_msb + i)) or (MAGIC.F_mem_out_of_bound(self, row, in2_msb + i)):
                    raise ValueError('trying to read memristor address outside row bound.')

                in1 = self.MAGIC[row][in1_msb + i]
                in2 = self.MAGIC[row][in2_msb + i]
                if (in1 + in2) == 1:
                    out = 1
                else:
                    out = 0
                MAGIC.__F_write_bit(self, row, out_add + i, out)

        MAGIC.F_update_counters(self)
        self.C_cycles += 5*n  # its takes 5 NOR iterations. initiation is done in calling function
        self.MAGIC[rows[0]].allocate(4 * n)  # 4 mid results to save
        MAGIC.F_update_counters(self)
        self.MAGIC[rows[0]].free(4 * n)
        MAGIC.F_update_counters(self)
    # end of function F_2num_XOR
    ##################################################

    ##################################################
    # function name: F_2num_AND
    # inputs:
    #   rows - vector with row numbers to execute bit AND on
    #   in1_msb  - address of first bit input
    #   in2_msb  - address of second bit input
    #   out_msb  - address of output bit
    #   n        - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   executing bit wise AND on two inputs on all given rows.
    #   inputs are the addresses of msbs memristors to execute the operation on
    #   updates counters accordingly
    def F_2num_AND(self, rows, in1_msb, in2_msb, out_add, n=-1):
        if n<0: n = self.N_bit
        rows = np.r_[rows]

        for row in rows:
            if (MAGIC.F_row_out_of_bound(self, row)):
                raise ValueError('trying to execute AND on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (
                row, len(self.MAGIC) - 1))
            for i in range(0, n):
                if (MAGIC.F_mem_out_of_bound(self, row, in1_msb + i)) or (MAGIC.F_mem_out_of_bound(self, row, in2_msb + i)):
                    raise ValueError('trying to read memristor address outside row bound.')

                in1 = self.MAGIC[row][in1_msb + i]
                in2 = self.MAGIC[row][in2_msb + i]
                if (in1 + in2) == 2:     out = 1
                else:                    out = 0
                MAGIC.__F_write_bit(self, row, out_add + i, out)

        MAGIC.F_update_counters(self)
        self.C_cycles += 3 * n  # its takes 3 NOR iterations. initiation is done in calling function
        self.MAGIC[rows[0]].allocate(2 * n)  # 2 mid results to save
        MAGIC.F_update_counters(self)
        self.MAGIC[rows[0]].free(2 * n)
        MAGIC.F_update_counters(self)
    # end of function F_2num_AND
    ##################################################

    ##################################################
    # function name: F_1num_NOT
    # inputs:
    #   rows - vector with row numbers to execute bit NOT on
    #   in_msb  - address of first bit input
    #   out_msb  - address of output bit
    #   n        - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   executing bit wise NOT on two inputs on all given rows.
    #   inputs are the addresses of msbs memristors to execute the operation on
    #   updates counters accordingly
    def F_1num_NOT(self, rows, in_msb, out_add, n=-1):
        if n<0: n = self.N_bit
        rows = np.r_[rows]

        for row in rows:
            if (MAGIC.F_row_out_of_bound(self, row)):
                raise ValueError('trying to execute NOT on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (
                row, len(self.MAGIC) - 1))
            for i in range(0, n):
                if (MAGIC.F_mem_out_of_bound(self, row, in_msb + i)):
                    raise ValueError('trying to read memristor address outside row bound.')

                in_val = self.MAGIC[row][in_msb + i]
                if in_val == 0:    out = 1
                else:              out = 0
                MAGIC.__F_write_bit(self, row, out_add + i, out)

        MAGIC.F_update_counters(self)
        self.C_cycles += 1 * n  # its takes 1 NOR iterations. initiation is done in calling function
        self.MAGIC[rows[0]].allocate(0)  # operates as NOR with one input
        MAGIC.F_update_counters(self)
        self.MAGIC[rows[0]].free(0)
        MAGIC.F_update_counters(self)
    # end of function F_1num_NOT
    ##################################################

    ##################################################
    # function name: F_2num_FA
    # inputs:
    #   rows          - vector with row numbers to execute FA on
    #   in1_msb       - address of first msb input
    #   in2_msb       - address of second msb input
    #   carry_in      - carry bit input - 0 or 1
    #   out_msb       - address of output msb
    #   carry_out_add - where to write carry out - default is to throw the carry away
    #   n             - numbers of bits representing the number (default: class.N_bits)
    #   one_bit_in2   - a flag to put only 1 bit in in2, to turn on: assign!=0
    # description:
    #   executing FA on two inputs on all given rows.
    #   inputs are the addresses of msbs memristors to execute the operation on
    #   update counters accordingly
    def F_2num_FA(self, rows, in1_msb, in2_msb, out_add, carry_in = 0, carry_out_add = -1, n= -1):
        # always use protection
        if n < 0: n = self.N_bit
        if (carry_in not in [0,1]): carry_in = 0

        rows = np.r_[rows]
        if MAGIC.F_row_out_of_bound(self, rows[len(rows)-1]):
            raise ValueError('trying to execute FA on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (row, len(self.MAGIC) - 1))
        for row in rows:
            [carry_out, bit_result] = [carry_in, 0]
            result = MemLine(n)
            for i in range(0, n):
                [carry_out, bit_result] = MAGIC.F_2bit_FA(self, row, in1_msb + n - 1 - i, in2_msb + n - 1 - i,carry_out)

                result.assign(n - 1 - i, bit_result)
                MAGIC.F_write_num(self, row, out_add, bin2dec(self.FIP, result), n)

            if carry_out_add > -1:
                MAGIC.__F_write_bit(self, row, carry_out_add, carry_out)

        # updating counters
        MAGIC.F_update_counters(self)
        self.C_cycles += cycle_FA(n)
        self.MAGIC[rows[0]].allocate(mem_FA(n))
        MAGIC.F_update_counters(self)
        self.MAGIC[rows[0]].free(mem_FA(n))
    # end of function F_2num_FA
    ##################################################

    ##################################################
    # function name: F_2bit_FA
    # inputs:
    #   row           - single row number to execute FA on
    #   in1_add       - address of bit input
    #   in2_add       - address of bit input
    #   carry_in      - carry bit input - 0 or 1
    # output:
    #   return a a 2X1 array of the [carry out, result]
    # description:
    #   executing bit FA on two inputs on all given rows.
    #   inputs are the addresses of bits memristors to execute the operation on
    #   !!!NOTE: this function does not update counters!!! to do so, use F_2num_FA (even for one line)
    def F_2bit_FA(self, row, in1_add, in2_add, carry_in=0):
        # always use protection
        if (MAGIC.F_mem_out_of_bound(self, row, in1_add) or MAGIC.F_mem_out_of_bound(self, row, in2_add)):
            raise ValueError('trying to read memristor address outside row bound.')
        if (carry_in not in [0, 1]): carry_in = 0
        result = self.MAGIC[row][in1_add] + self.MAGIC[row][in2_add] + carry_in
        if result > 1:
            carry_out = 1
            if result == 2:   result = 0
            else:             result = 1
        else:
            carry_out = 0
        return [carry_out, result]
    # end of function F_2bit_FA
    ##################################################

    ##################################################
    # function name: F_ADD1bit
    # inputs:
    #   rows          - vector with row numbers to execute FA on
    #   in1_msb       - address of first msb input
    #   carry_in      - carry bit input - 0 or 1
    #   out_add       - address of output msb
    #   carry_out_add - where to write carry out - default is to throw the carry away
    #   n             - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   adding 1 bit to a number, using HA's.
    #   inputs are the addresses of msb's memristors and carry in (bit, not address)  to execute the operation on
    #   update counters accordingly
    def F_ADD1bit(self, rows, in1_msb, bit_in2, out_add, carry_out_add = -1, n= -1):
        # always use protection
        if n < 0: n = self.N_bit

        rows = np.r_[rows]
        if MAGIC.F_row_out_of_bound(self, rows[len(rows)-1]):
            raise ValueError('trying to execute ADD1bit on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (row, len(self.MAGIC) - 1))

        for row in rows:

            carry_out = self.MAGIC[row][bit_in2]
            result = MemLine(n)
            for i in range(0, n):
                [carry_out, bit_result] = MAGIC.F_2bit_HA(self, row, in1_msb + n - 1 - i, carry_out, value_in2=1)
                result.assign(n - 1 - i, bit_result)
                MAGIC.F_write_num(self, row, out_add, bin2dec(self.FIP, result), n)

            if carry_out_add > -1:
                MAGIC.__F_write_bit(self, row, carry_out_add, carry_out)

        # updating counters
        MAGIC.F_update_counters(self)
        self.C_cycles += cycle_ADD1bit(n)
        self.MAGIC[rows[0]].allocate(mem_ADD1bit(n))
        MAGIC.F_update_counters(self)
        self.MAGIC[rows[0]].free(mem_ADD1bit(n))
        MAGIC.F_update_counters(self)
    # end of function F_ADD1bit
    ##################################################

    ##################################################
    # function name: F_2bit_HA
    # inputs:
    #   row           - single row number to execute FA on
    #   in1_add       - address of bit input
    #   in2_add       - address of bit input
    # output:
    #   return a a 2X1 array of the [carry out, result]
    # description:
    #   executing bit FA on two inputs on all given rows.
    #   inputs are the addresses of bits memristors to execute the operation on
    #   !!!NOTE: this function does not update counters!!! to do so, use F_2num_FA (even for one line)
    def F_2bit_HA(self, row, in1_add, in2, value_in2=0):
        # always use protection
        if MAGIC.F_mem_out_of_bound(self, row, in1_add):
            raise ValueError('trying to read memristor address outside row bound.')

        if value_in2 != 0:
            if in2 not in [0,1]:
                raise ValueError('in2 has invalid value: not in [0,1].')
            result = self.MAGIC[row][in1_add] + in2
        else:
            if MAGIC.F_mem_out_of_bound(self, row, in2):
                raise ValueError('trying to read memristor address outside row bound.')
            result = self.MAGIC[row][in1_add] + self.MAGIC[row][in2]

        if result > 1:
            carry_out = 1
            result = 0
        else:
            carry_out = 0
        return [carry_out, result]
    # end of function F_2bit_HA
    ##################################################

    ##################################################
    # function name: F_abs
    # inputs:
    #   rows          - vector with row numbers to execute FA on
    #   in_msb        - address of first msb input
    #   out_msb       - address of output msb
    #   n             - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   executing abs function on the given input on all given rows.
    #   input are the addresses of msb memristor to execute the operation on
    #   executing the operation according to 2's complement convention
    #   msb bit is the sign bit
    #   uses F_invert_according2sign which updates the counters
    def F_abs(self, rows, in_msb, out_add, n=-1):
        MAGIC.F_invert_according2sign(self, rows, in_msb, in_msb, out_add, n=n)
    #end of function F_abs
    #################################################

    ##################################################
    # function name: F_invert_according2sign
    # inputs:
    #   rows          - vector with row numbers to execute FA on
    #   sign_add      - address of sign to invert according to
    #   in_msb        - address of first msb input
    #   out_msb       - address of output msb
    #   n             - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   executing invert function on the given input on all given rows.
    #   input are the addresses of msb memristor to execute the operation on
    #   executing the operation according to 2's complement convention
    #   sign_add is the sign bit address to invert according to (1 invert, 0 don't invert)
    #   update counters accordingly
    def F_invert_according2sign(self, rows, sign_add, in_msb, out_add, n=-1):
        # always use protection
        if n < 0: n = self.N_bit
        rows = np.r_[rows]

        # making sure out_add won't be run over by mid_result
        for row in rows:
            MAGIC.F_write_num(self, row, out_add, 0)

        # allocating memristors to mid result will be done at the end of the memristors line by 2num_XOR
        mid_res_msb = len(self.MAGIC[rows[0]])

        # execute XOR of every bit with sign bit to a mid result
        # initiate the memristor used for this operation in single cycle
        self.C_cycles +=1
        for i in range(0, n):
            MAGIC.F_2num_XOR(self, rows, sign_add, in_msb + i, mid_res_msb + i, n=1)

        MAGIC.F_ADD1bit(self, rows, mid_res_msb, sign_add, out_add, n=n)

        # updating counters
        MAGIC.F_update_counters(self)
        # free allocated memristors
        for row in rows:
            self.MAGIC[row].free(n)
        MAGIC.F_update_counters(self)

    # end of function F_invert_according2sign
    ##################################################

    ##################################################
    # function name: F_2num_MUL
    # inputs:
    #   rows          - vector with row numbers to execute MUL on
    #   in1_msb       - address of first msb input
    #   in2_msb       - address of second msb input
    #   out_add       - address of output msb
    #   n             - number of bits representing the input numbers (default: class.N_bits)
    #   res_n         - number of bits representing the output number (default: class.N_bits)
    #   p             - number of bits representing the resolution of the input numbers (default: class.FIP)
    #   res_p         - number of bits representing the resolution of the output number (default: class.FIP)
    # description:
    #   executing multiplication on two inputs on all given rows.
    #   inputs are the addresses of msbs memristors to execute the operation on
    #   update counters accordingly
    def F_2num_MUL(self, rows, in1_msb, in2_msb, out_add, n= -1, res_n=-1, p=-1, res_p=-1):
        # always use protection
        if n < 0: n = self.N_bit
        if res_n < 0: res_n = n
        if p < 0: p = self.FIP
        if res_p < 0: res_p = p

        rows = np.r_[rows]

        if MAGIC.F_row_out_of_bound(self, rows[len(rows)-1]):
            raise ValueError('trying to execute NOT on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (row, len(self.MAGIC) - 1))
        if MAGIC.F_mem_out_of_bound(self, rows[0], in1_msb+n-1) or MAGIC.F_mem_out_of_bound(self, rows[0], in2_msb+n-1) or (in1_msb<0 or in2_msb<0):
            raise ValueError('trying to read memristor address outside row bound.')

        for row in rows:
            num1 = MAGIC.F_read_num(self, row, in1_msb, n, p)
            num2 = MAGIC.F_read_num(self, row, in2_msb, n, p)
            MAGIC.F_write_num(self, row, out_add, num1*num2, res_n, res_p)

        MAGIC.F_update_counters(self)
        self.C_cycles += cycle_MUL(n)
        self.MAGIC[rows[0]].allocate(mem_MUL(n))
        MAGIC.F_update_counters(self)
        self.MAGIC[rows[0]].free(mem_MUL(n))
        MAGIC.F_update_counters(self)
    # end of function F_2num_MUL
    ##################################################

    ##################################################
    # function name: F_2num_DIV_remain
    # inputs:
    #   rows          - vector with row numbers to execute MUL on
    #   numerator_add - address of numerator msb
    #   divisor_add   - address of divisor msb
    #   result_add    - address of result msb
    #   remain_add    - address of remain msb
    # description:
    #   executing fixed point division on two inputs on all given rows.
    #   dividing numerator with divisor
    #   result and remain will be written to given addresses
    #   assuming N and p constant
    #   update counters accordingly
    def F_2num_DIV_remain(self, rows, numerator_add, divisor_add, result_add, remain_add):
        # always use protection
        rows = np.r_[rows]
        if MAGIC.F_row_out_of_bound(self, rows[len(rows)-1]):
            raise ValueError('trying to execute NOT on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (row, len(self.MAGIC) - 1))
        N = self.N_bit
        p = self.FIP

        if MAGIC.F_mem_out_of_bound(self, rows[0], numerator_add+N-1) or MAGIC.F_mem_out_of_bound(self, rows[0], divisor_add+N-1) or (numerator_add<0 or divisor_add<0):
            raise ValueError('trying to read memristor address outside row bound.')
        ############################
        # INITIATING ALGORITHM
        ############################
        # eventually, at the end of initiation phase, memristor line will be 14N-5 memristors long and contain this in order:
        # 1. numerator          = N [mems]
        # 2. divisor            = N [mems]
        # 3. result             = N [mems]
        # 4. remain             = N [mems]
        # 5. result sign        = 1 [mems]
        # 6. mid numerator1     = 2N-1 [mems]
        # 7. mid numerator2     = 2N-1 [mems]
        # 8. mid divisor        = 3N-2 [mems]
        # 9. mid NOT divisor    = 3N-2 [mems]
        ############################

        # initiate all memristos for later use:
        self.C_cycles += 1

        # allocate memrisotrs for result and remain
        for row in rows:
            MAGIC.F_write_num(self, row, result_add, 0)
            MAGIC.F_write_num(self, row, remain_add, 0)

        # keep track of numerator sign bit and result sign bit
        numerator_sign_bit_add = numerator_add
        result_sign_bit_add = len(self.MAGIC[rows[0]])
        MAGIC.F_2num_XOR(self, rows, numerator_add, divisor_add, result_sign_bit_add, n=1) # writing the sign of the result

        # allocate memristors for 2Xmid-numerator & mid-divisor & mid-NOT-divisor
        mid_numerator_add1 = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, mid_numerator_add1, 0, n=(2 * N - 1))
        mid_numerator_add2 = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, mid_numerator_add2, 0, n=(2 * N - 1))

        mid_divisor_add = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, mid_divisor_add, 0, n=(3 * N - 2))

        mid_NOT_divisor_add = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, mid_NOT_divisor_add, 0, n=(3 * N - 2))


        # since we are working with positive numebrs only, we transform the inputs to positive stright to their place
        MAGIC.F_abs(self, rows, numerator_add, mid_numerator_add1 + N -1)
        MAGIC.F_abs(self, rows, divisor_add, mid_divisor_add + N - 1)

        # initiate all memristos for mid_NOT_divisor:
        self.C_cycles += 1

        # prepare NOT divisor as well
        MAGIC.F_1num_NOT(self, rows, mid_divisor_add, mid_NOT_divisor_add, n=(3*N-2))

        # print "MAGIC after initation phase in division function:"
        # self.F_print()

        ########################################################
        # INITIATING ALGORITHM - DONE - START ITERATIONS PHASE
        ########################################################
        # in this phase we subtract the divisor from mid_numerator
        # each subtraction is in decreasing scale, starting from MSB
        # then we take the sign of the result and NOT it into its place in final result
        mid_AND_result_add = len(self.MAGIC[rows[0]])  # we will need it to return to correct numerator

        counter = N-1
        for i in range(counter,-1,-1):
            # initiate all memristos for later use:
            self.C_cycles += 1

            MAGIC.F_2num_FA(self, rows, mid_numerator_add1, mid_NOT_divisor_add + i, mid_numerator_add2, carry_in=1 , n= (2*N-1)) #subtraction
            # print "MAGIC after subtractioin in division function, i = ", i
            # self.F_print()

            MAGIC.F_1num_NOT(self, rows, mid_numerator_add2, result_add + (N - 1) - i, n=1) # writing correct bit to its place
            # print "MAGIC after bit not of result in division function, i = ", i
            # self.F_print()

            # executing AND operation bit on nid_num sign bit with mid_div
            # using NOR operations on bit we already have
            # memristors were already initalized
            for j in range (0, 2*N-1):
                MAGIC.F_2num_NOR(self, rows, result_add + (N - 1) - i, mid_NOT_divisor_add + i + j, mid_AND_result_add + j, n=1)

            # initiate all memristos for later use:
            self.C_cycles += 1

            MAGIC.F_2num_FA(self, rows, mid_numerator_add2, mid_AND_result_add, mid_numerator_add1, n=(2 * N - 1))  # returning to correct numerator
            # print "MAGIC after addition in division function, i = ", i
            # self.F_print()

        # freeing the AND reseult allocated for this phase (2N-1) + mid div (3N-2) + NOT mid div (3N-2) + mid num2 (2N-1)
        for row in rows:
            self.MAGIC[row].free(10*N-6)

        # print "MAGIC end of iteration phase"
        # self.F_print()
        ########################################################
        # ITERATION ALGORITHM - DONE - START EPILOGUE PHASE
        ########################################################
        # invert result according to its sign bit
        # invert remain according to numerator sign bit
        # free all unnecessary memristors

        # preparing place for invert result
        invert_result_add = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, invert_result_add, 0)
        temp_add = len(self.MAGIC[rows[0]])
        MAGIC.F_1num_NOT(self, rows, result_add, temp_add)
        MAGIC.F_1num_NOT(self, rows, temp_add, invert_result_add)
        for row in rows:
            self.MAGIC[row].free(N)

        MAGIC.F_invert_according2sign(self, rows, result_sign_bit_add, invert_result_add, result_add)

        MAGIC.F_invert_according2sign(self, rows, numerator_sign_bit_add, mid_numerator_add1 + N -1, remain_add)

        for row in rows:
            self.MAGIC[row].free(3*N) # invert result (N) + mid_num1 (2N-1) + result sign bit (1)
    # end of function F_2num_DIV_remain
    ##################################################

    ##################################################
    # function name: F_2num_DIV_approx
    # inputs:
    #   rows          - vector with row numbers to execute MUL on
    #   numerator_add - address of numerator msb
    #   divisor_add   - address of divisor msb
    #   result_add    - address of result msb
    #   N             - the N bit representation of result, default is N of simulation
    #   p             - the p of fixed ponit of result, default is p of simulation
    # description:
    #   executing fixed point division on two inputs on all given rows.
    #   dividing numerator with divisor
    #   result will be written to given addresses at a given resolution (or default as simulation resolution)
    #   assuming N and p constant
    #   update counters accordingly
    def F_2num_DIV_approx(self, rows, numerator_add, divisor_add, result_add, N = -1, p =-1):
        # always use protection
        rows = np.r_[rows]
        if MAGIC.F_row_out_of_bound(self, rows[len(rows)-1]):
            raise ValueError('trying to execute NOT on row out of bound. row = %d, while MAGIC has rows 0 to %d' % (row, len(self.MAGIC) - 1))
        if N<0: N = self.N_bit # we will use this N as N(new)
        if p<0: p = self.FIP
        if N<p: N_new = p + 1
        else  : N_new = N
        N_old = self.N_bit


        if MAGIC.F_mem_out_of_bound(self, rows[0], numerator_add+N_old-1) or MAGIC.F_mem_out_of_bound(self, rows[0], divisor_add+N_old-1) or (numerator_add<0 or divisor_add<0):
            raise ValueError('trying to read memristor address outside row bound.')
        ############################
        # INITIATING ALGORITHM
        ############################
        # eventually, at the end of initiation phase, memristor line will be 13N+6p-5 memristors long and contain this in order:
        # 1. numerator          = N(old) [mems]
        # 2. divisor            = N(old) [mems]
        # 3. result             = N(new) [mems]
        # 4. result sign        = 1 [mems]
        # 5. mid numerator1     = 2N(old)-1+p(new) [mems]
        # 6. mid numerator2     = 2N(old)-1+p(new) [mems]
        # 7. mid divisor        = 3N(old)-2 [mems]
        # 8. mid NOT divisor    = 3N(old)-2 [mems]
        ############################

        # initiate all memristos for later use:
        self.C_cycles +=1
        # allocate memrisotrs for result with given N and p
        for row in rows:
            MAGIC.F_write_num(self, row, result_add, 0, n=N_new, p=p)

        # keep track of numerator sign bit and result sign bit
        numerator_sign_bit_add = numerator_add
        result_sign_bit_add = len(self.MAGIC[rows[0]])
        MAGIC.F_2num_XOR(self, rows, numerator_add, divisor_add, result_sign_bit_add, n=1) # writing the sign of the result

        # allocate memristors for 2Xmid-numerator & mid-divisor & mid-NOT-divisor
        mid_numerator_add1 = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, mid_numerator_add1, 0, n=(2 * N_old + p - 1))

        mid_numerator_add2 = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, mid_numerator_add2, 0, n=(2 * N_old + p - 1))

        mid_divisor_add = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, mid_divisor_add, 0, n=(3 * N_old - 2))

        mid_NOT_divisor_add = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, mid_NOT_divisor_add, 0, n=(3 * N_old - 2))

        # since we are working with positive numebrs only, we transform the inputs to positive straight to their place
        # note that the msb is going into position N+1 and the rest are zeros
        # for example, number 8 in N(old)=N(new)=7, p(old)=p(new)2 will look like this:
        # address 0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15
        # bit     0  0  0  0  0  0  0  1  0  0  0  0  0  0  0  0
        # where bits 0-5 are always zeros,
        # bit 6 is the sign bit,
        # bits 7-13 is the abs of the number,
        # and bits 14-15 are the added p (also always zero)
        MAGIC.F_abs(self, rows, numerator_add, mid_numerator_add1 + N_old -1)
        # divisor goes in the middle of a 3N-2 bits
        MAGIC.F_abs(self, rows, divisor_add, mid_divisor_add + N_old - 1)

        # initiate all memristos for mid_NOT_divisor:
        self.C_cycles += 1
        # prepare NOT divisor as well
        MAGIC.F_1num_NOT(self, rows, mid_divisor_add, mid_NOT_divisor_add, n=(3 * N_old - 2))

        # print "MAGIC after initation phase in division function:"
        # self.F_print()

        ########################################################
        # INITIATING ALGORITHM - DONE - START ITERATIONS PHASE
        ########################################################
        # in this phase we subtract the divisor from mid_numerator
        # each subtraction is in decreasing scale, starting from MSB
        # then we take the sign of the result and NOT it into its place in final result
        mid_AND_result_add = len(self.MAGIC[rows[0]])  # we will need it to return to correct numerator
        for row in rows:
            MAGIC.F_write_num(self, row, mid_AND_result_add, 0, n=(2 * N_old - 1))
        thrown_sign_bit_add = len(self.MAGIC[rows[0]])  # we will need it when we are throwind bits out of oue N representation
        for row in rows:
            MAGIC.F_write_num(self, row, thrown_sign_bit_add, 0, n=1, p=0)
        ######################################################
        #       first iteration block
        ######################################################
        counter = N_old - 1
        for i in range(counter, -1 ,-1):
            #intiate memristors for next operation
            self.C_cycles +=1
            MAGIC.F_2num_FA(self, rows, mid_numerator_add1, mid_NOT_divisor_add + i, mid_numerator_add2, carry_in=1 , n= (2*N_old -1)) #subtraction
            # print "MAGIC after subtraction in division function, i = ", i
            # self.F_print()

            # write only bits that are inside N(new), the rest drops.
            # because it is done by controller it is possible to use "if" statement

            if (i < N_new - p - 1):
                # index of writing to result is counted from LSB
                MAGIC.F_1num_NOT(self, rows, mid_numerator_add2, result_add + (N_new - 1) - p - i, n=1) # writing correct bit to its place
                # print "MAGIC after bit not of result in division function, i = ", i
                # self.F_print()
            else:
                MAGIC.F_1num_NOT(self, rows, mid_numerator_add2, thrown_sign_bit_add,n=1)  # writing correct bit to its place
                # print "MAGIC after bit not of result thrown in division function, i = ", i
                # self.F_print()

            # executing AND operation bit on mid_num sign bit with mid_div
            # using NOR operations on inverted bits we already have - thus implementing AND
            # initiating memristors was already done

            for j in range (0, 2 * N_old -1):
                if (i < N_new - p - 1):
                    # index of correct bit from result is counted from LSB
                    MAGIC.F_2num_NOR(self, rows, result_add + (N_new - 1) - p - i, mid_NOT_divisor_add + i + j, mid_AND_result_add + j, n=1)
                else:
                    MAGIC.F_2num_NOR(self, rows, thrown_sign_bit_add, mid_NOT_divisor_add + i + j, mid_AND_result_add + j, n=1)

            # intiate memristors for next operation
            self.C_cycles += 1
            MAGIC.F_2num_FA(self, rows, mid_numerator_add2, mid_AND_result_add, mid_numerator_add1, n=(2 * N_old - 1))  # returning to correct numerator
            # print "MAGIC after addition in division function, i = ", i
            # self.F_print()
        # print "MAGIC after 1st iteration stage in division function"
        # self.F_print()

        ######################################################
        #       second iteration block
        ######################################################
        for i in range(-1 , -1-p , -1):
            # intiate memristors for next operation
            self.C_cycles += 1
            MAGIC.F_2num_FA(self, rows, mid_numerator_add1 + N_old - 1, mid_NOT_divisor_add + i + (N_old - 1), mid_numerator_add2 + N_old - 1, carry_in=1, n=(N_old + p))  # subtraction
            # print "MAGIC after subtractioin in division function, i = ", i
            # self.F_print()

            # write only bits that are inside N(new), the rest drops.
            # because it is done by controller it is possible to use "if" statment
            # initiating memristors was already done

            MAGIC.F_1num_NOT(self, rows, mid_numerator_add2 + N_old - 1, result_add + (N_new - 1) - p - i, n=1)  # writing correct bit to its place
            # print "MAGIC after bit not of result in division function, i = ", i
            # self.F_print()

            # executing AND operation bit on mid_num sign bit with mid_div
            # using NOR operations on inverted bits we already have - thus implementing AND
            # initiating memristors was already done

            for j in range(0, N_old + p):
                # index of writing to result is counted from LSB
                MAGIC.F_2num_NOR(self, rows, result_add + (N_new - 1) - p - i, mid_NOT_divisor_add + i + j + (N_old - 1), mid_AND_result_add + j, n=1)

            # intiate memristors for next operation
            self.C_cycles += 1
            MAGIC.F_2num_FA(self, rows, mid_numerator_add2 + N_old - 1, mid_AND_result_add, mid_numerator_add1 + N_old - 1, n=(N_old + p ))  # returning to correct numerator

            # print "MAGIC after addition in division function, i = ", i
            # self.F_print()
        # print "MAGIC after 2nd iteration stage in division function"
        # self.F_print()

        # freeing allocated memristors for this phase:
        # AND allocated for this phase (2N-1)
        # + mid div                    (3N-2)
        # + NOT mid div                (3N-2)
        # + mid num1                   (2N+p-1)
        # + mid num2                   (2N+p-1)
        # + thrown_sign_bit_add        (1)
        for row in rows:
            self.MAGIC[row].free(12*N_old+2*p-6)
            #self.MAGIC[row].free(12 * N_old + 7 * p - 6)

        # print "MAGIC end of iteration phase"
        # self.F_print()

        # #######################################################
        # ITERATION ALGORITHM - DONE - START EPILOGUE PHASE
        ########################################################
        # invert result according to its sign bit
        # invert remain according to numerator sign bit
        # free all unnecessary memristors

        # preparing place for invert result
        # initiating memristors was already done in last iteration

        invert_result_add = len(self.MAGIC[rows[0]])
        for row in rows:
            MAGIC.F_write_num(self, row, invert_result_add, 0, n=N_new)
        temp_add = len(self.MAGIC[rows[0]])
        MAGIC.F_1num_NOT(self, rows, result_add, temp_add, n=N_new)
        MAGIC.F_1num_NOT(self, rows, temp_add, invert_result_add, n=N_new) # we can do better if we won't use the invert_according2sign function
        for row in rows:
            self.MAGIC[row].free(N_new) # free temp

        MAGIC.F_invert_according2sign(self, rows, result_sign_bit_add, invert_result_add, result_add, n=N_new)

        for row in rows:
            self.MAGIC[row].free(N_new + 1) # invert result (N) + result sign bit (1)

    # end of function F_2num_DIV_approx
    ##################################################