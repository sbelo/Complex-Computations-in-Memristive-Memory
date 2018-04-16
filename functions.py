import random as rand
import numpy as np
import sys
from mem_line import MemLine

##########################################################################
## change_sign:
# mem - the wanted number (bit representation) to be inverted
# description: returns a MemLine containing the sign changed number represented in vec
def change_sign(mem):
    length = len(mem)
    temp = mem.invert(0,length)
    carry = 1
    for i in range(0, length):
        if carry == 0:
            break
        else:
            if temp[length - 1 - i] == 1:
                temp[length - 1 - i] = 0
                carry = 1
            else:
                temp[length - 1 - i] = 1
                carry = 0
    return temp
# end of change_sign
##########################################################################

##########################################################################
## bin2dec:
# p- number of bits representing the fraction
# mem - the wanted number (bit represented in MemLine object) to be converted to decimal
# description: returns a a float containing the number represented in mem
def bin2dec(p, mem):
    length = len(mem)
    # check if the number is negative:
    if mem[0] > 0:
        neg = 1
        # change number to positive:
        temp = change_sign(mem)
    else:
        neg = 0
        # make sure we don't change the original number:
        temp = mem.deep_copy()
    # divide the MemLine object to an integer and a fraction:
    mem_fraction = temp[slice(length - p , length)]
    mem_whole = temp[slice(0, length - p )]
    whole = 0
    for i in range(0, len(mem_whole)):
        # every iteration add the decimal value of the current bit:
        whole += (mem_whole[len(mem_whole)-1-i])*pow(2, i)
    fraction = 0
    for j in range(0, p):
        # every iteration add the decimal value of the current bit:
        fraction += (mem_fraction[j])*pow(2, -(j+1))
    # add the 2 numbers to get the result:
    result = whole + fraction
    # return the result according to its sign at the beginning
    if neg == 0:
        return result
    else:
        return -result
# end of bin2dec
##########################################################################

##########################################################################
## dec2bin:
# n- length of number in bits
# p- number of bits representing the fraction
# num - the wanted number to be converted
# description: returns a MemLine object containing the bit representation of num in bits
def dec2bin(n, p, num):
    # allocate 2 MemLine objects, one for the fracture and the other for the integer
    mem_fraction = MemLine(p)
    mem_whole = MemLine(n - p)
    # sign check:
    if num < 0:
        num = -num
        neg = 1
    else:
        neg = 0
    whole = int(num)
    fraction = num - whole
    # calculate the fraction part and assign it:
    for i in range(0, p):
        temp = fraction * 2
        curr_bit = int(temp)
        fraction = temp - curr_bit
        mem_fraction[i] = curr_bit
    #calculate the whole part:
    for j in range(0, n - p):
        curr_bit = whole % 2
        whole = int(whole / 2)
        mem_whole[n - p - 1 - j] = curr_bit
    result = mem_whole + mem_fraction
    # convert result to the right sign
    if neg == 0:
        return result
    else:
        return change_sign(result)
#end of dec2bin
##########################################################################

##########################################################################
def randrange_float(start, stop, step):
    return rand.randint(0, int((stop - start) / step)) * step + start
##########################################################################

##########################################################################
## print_equation:
# equation_func - a tuple output by polyfit that represents an equation
# arg - a char representing the variable ('N' , 'P')
# description: prints polyfit output in a format of "AN^k + BN^(k-1) + ... + CN^1 + D"
def print_equation(equation_func, arg):
    equation_degree = len(equation_func) - 1
    i = equation_degree
    while i >= 0:
        if abs(equation_func[equation_degree - i]) < 0.0001 :
            i = i - 1
        else:
            if i == 0:
                print "%.2f" % abs(equation_func[equation_degree - i])
                break
            else:
                print "%.2f" % equation_func[equation_degree - i],
                sys.stdout.write(arg)
                print "^%d" %  i,
                break

    for j in reversed(range(i)):
        if equation_func[equation_degree - j] < 0:
            print "-",
        else:
            print "+",

        if j == 0:
            print "%.2f" % abs(equation_func[equation_degree - j])
        else:
            print "%.2f" % abs(equation_func[equation_degree - j]),
            sys.stdout.write(arg)
            print "^%d" % j,
# end of print_equation
##########################################################################