
import BitVector
from BitVector import BitVector
import numpy as np
########################################


## to declare a memory object:
# new_mem = MemLine(6) 
# this sets a memory in the length 6, default is 0.
class MemLine:
    ######################################################################
    ## initiation:
    # n - the size of the line (default is 0)
    # description:
    # initiates a MemLine object in the wanted size.
    def __init__(self, n = 0):
        self.__data = BitVector(size = n)
    # end of initiation function
    ######################################################################

    ######################################################################
    # __getitem__:
    # i - index or a slice
    # description:
    # returns the bit in the wanted index of the MemLine object, or a MemLine object
    # containing the slice (if i is a slice)
    # in case of slice input, can only handle steps of 1!!!!
    def __getitem__(self, i):
        if isinstance(i, slice):
            if i.start < 0 or i.stop > self.__len__() or i.start >= i.stop:
                return -1
            else:
                new = MemLine(i.stop - i.start)
                new.__data = self.__data[i]
                return new
        else:
            if i >= self.__data.__len__() or i < 0:
                return -1
            else:
                return self.__data[i]
    # end of __getitem__
    ######################################################################

    ######################################################################
    # __setitem__ :
    # i     - index
    # value - a bit to assign, 0 or 1
    # description:
    # sets the argument in the 'i' index to value
    def __setitem__(self, i, value):
        if i >= self.__data.__len__() or i < 0:
            return -1
        else:
            self.__data.__setitem__(i, value)
            return 0
    # end of __setitem__
    ######################################################################

    ######################################################################
    ## __add__:
    # rhs - a MemLine object
    # description:
    # returns a MemLine object that contains the self followed by rhs
    def __add__(self, rhs):
        sum = MemLine(self.__len__() + rhs.__len__())
        sum.__data = self.__data + rhs.__data
        return sum
    # end of __add__
    ######################################################################

    ######################################################################
    ## __len__:
    # description:
    # returns the length of the MemLine object, aka the current memory usage
    def __len__(self):
        return self.__data.__len__()
    # end of __len__
    ######################################################################

    ######################################################################
    ## deep_copy:
    # description:
    # returns a "hard" copy of the current MemLine object
    def deep_copy(self):
        new_mem = MemLine(self.__data.__len__())
        new_mem.__data = self.__data.deep_copy()
        return new_mem
    # end of deep_copy
    ######################################################################

    ######################################################################
    ## invert:
    # i- start index
    # n- length of num
    # description: returns the inversion of a vector in n length
    # that starts in index 'i' in the memory.
    def invert(self, i, n):
        pos = slice(i, i + n)
        inv = MemLine(n)
        inv.__data = self.__data[pos].__invert__()
        return inv
    ######################################################################

    ######################################################################
    ## assign:
    # i- start index
    # vec- vector to assign
    # description: assignes vec to the memory, strating at index i
    def assign(self, i, value):
        if i  >= self.__data.__len__() or i < 0 :
            return -1
        else:
            self.__setitem__(i, value)
            return 0
    # end of assign
    ######################################################################

    ######################################################################
    ## allocate:
    # n- number of bits wanted to be allocated
    # description: allocates memory in size of n to the end of the memory.
    def allocate(self, n = 1):
        temp = self.__data + BitVector(size=n)
        self.__data = temp
    # end of allocate
    ######################################################################

    ######################################################################
    ## free:
    # n- number of bits wanted to be freed
    # description: frees n bits from the end of the memory
    def free(self, n):
        temp = self.__data[slice(0, self.__data.__len__() - n)]
        self.__data = temp
    # end of free
    ######################################################################

    ######################################################################
    ## print_mem:
    # description: prints the MemLine.
    def print_mem(self):
        print self.__data
    # end of print_mem
    ######################################################################
