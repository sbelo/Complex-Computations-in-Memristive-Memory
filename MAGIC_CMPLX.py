
##################################################
#                   imports
##################################################
from MAGIC import MAGIC


# end of imports
##################################################

class MAGIC_CMPLX(MAGIC):
    ##################################################
    # function name: F_write_num
    # inputs:
    #   row_address - the row address in memory where to write to
    #   msb_address - column address to write MSB input to
    #   cmplx_num   - an array in a size of 2 that the first argument is the real value and the second is the imaginary value
    #   n           - numbers of bits representing the number (default: class.N_bits)
    #   p           - numbers of bits representing the resolution of the number (default: class.FIP)
    # outputs:
    # description:
    #   writing a number into MAGIC array.
    #   input MSB & output MSB are given as inputs.
    #   N - size of bits representing the number is a parameter given.
    #   the function also updating counters accordingly.
    def F_write_CMPLX_num(self, row_address, msb_address, cmplx_num, n=-1, p=-1):
        if n < 0: n = self.N_bit
        MAGIC.F_write_num(self, row_address, msb_address, cmplx_num[0], n, p)
        MAGIC.F_write_num(self, row_address, msb_address + n, cmplx_num[1], n, p)
    # end of function F_write_num
    ##################################################

    ##################################################
    # function name: F_read_num
    # inputs:
    #   row_address - the row address in memory where to read from
    #   msb_address - the column address where the MSB to read from
    #   n           - numbers of bits representing the number (default: class.N_bits)
    #   p           - numbers of bits representing the resolution of the number (default: class.FIP)
    # outputs:
    #   cmplx_num - an array containing the real and imaginary parts as float numbers read from memory according to its address
    # description:
    #
    def F_read_num(self, row_address, msb_address, n=-1, p=-1):
        if n < 0: n = self.N_bit
        cmplx_num = []
        cmplx_num.append(MAGIC.F_read_num(self, row_address, msb_address, n, p))
        cmplx_num.append(MAGIC.F_read_num(self, row_address, msb_address + n, n, p))
        return cmplx_num

    # end of function F_read
    ##################################################

    ##################################################
    # function name: F_2num_FA
    # inputs:
    #   rows          - vector with row numbers to execute FA on
    #   in1_msb       - address of first msb input
    #   in2_msb       - address of second msb input
    #   carry_in      - an array containing 2 arguments, [0] for real carry, and [1] for imaginary carry
    #   out_msb       - address of output msb
    #   carry_out_add - where to write carry out (need to have 2 free memory cells, on for the real and one for the imaginary)
    #                           - default is to throw the carry away
    #   n             - numbers of bits representing the number (default: class.N_bits)
    # description:
    #   executing FA on two inputs on all given rows.
    #   inputs are the addresses of msbs memristors to execute the operation on
    #   update counters accordingly
    def F_2num_FA(self, rows, in1_msb, in2_msb, out_add, carry_in=[0,0], carry_out_add=-1, n=-1):
        if n < 0: n = self.N_bit

        # calculating the real part:
        MAGIC.F_2num_FA(self, rows, in1_msb, in2_msb, out_add, carry_in[0], carry_out_add, n)

        # if we need to write the carry_out, need to advance it to the imaginary "place":
        if carry_out_add >= 0:
            carry_out_add += 1

        # calculating the imaginary part:
        MAGIC.F_2num_FA(self, rows, in1_msb + n, in2_msb + n, out_add + n, carry_in[1], carry_out_add, n)

    # end of function F_2num_FA
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
    def F_2num_MUL(self, rows, in1_msb, in2_msb, out_add, n=-1, res_n=-1, p=-1, res_p=-1):

        # check n and res_n since we need them in this function:
        if n < 0: n = self.N_bit
        if res_n < 0: res_n = self.N_bit

        # allocate memory for the result:
        for row in rows:
            self.F_write_CMPLX_num(row, out_add, [0,0], n=res_n)

        mid_res_i = len(self.MAGIC[rows[0]])

        # initiating mid result memristors:
        self.C_cycles += 1

        # calculate the multiplication of the 2 Imaginary parts:
        MAGIC.F_2num_MUL(self, rows, in1_msb + n, in2_msb + n, mid_res_i, n, res_n, p, res_p)
        # inverting the result (will help later to change sign):
        MAGIC.F_1num_NOT(self, rows, mid_res_i, mid_res_i + res_n, res_n)

        #initiating mid result memristors:
        self.C_cycles += 1

        # calculate the multiplication of the 2 Real parts:
        MAGIC.F_2num_MUL(self, rows, in1_msb, in2_msb, mid_res_i, n, res_n, p, res_p)
        # adding 1 multiplication, an the inversion of the other with carry_in=1 creates subtraction;
        MAGIC.F_2num_FA(self, rows, mid_res_i, mid_res_i + res_n, out_add, carry_in=1, n=res_n)

        # initiating mid result memristors:
        self.C_cycles += 1

        # calculate the multiplication of the 2 Imaginary part mid results, and adding them together:
        MAGIC.F_2num_MUL(self, rows, in1_msb, in2_msb + n, mid_res_i, n, res_n, p, res_p)

        MAGIC.F_2num_MUL(self, rows, in1_msb + n, in2_msb, mid_res_i + res_n, n, res_n, p, res_p)

        MAGIC.F_2num_FA(self, rows, mid_res_i, mid_res_i + res_n, out_add + res_n, n=res_n)
        for i in rows:
            self.MAGIC[i].free(2*res_n)
    # end of function F_2num_MUL
    ##################################################

    ##################################################
    # function name: F_2num_DIV_remain
    # inputs:
    #   rows          - vector with row numbers to execute MUL on
    #   numerator_add - address of numerator msb
    #   divisor_add   - address of divisor msb
    #   out_add       - address of result msb
    #   remain_add    - address of remain msb
    #   n             - the number of bits representing each Re/Im number of the inputs
    #   res_n         - the number of bits representing each Re/Im number of the output
    #   p             - the number of bits representing each Re/Im number FIP of the inputs
    #   res_p         - the number of bits representing each Re/Im number FIP of the output
    # description:
    #   executing fixed point division on two inputs on all given rows.
    #   dividing numerator with divisor
    #   result and remain will be written to given addresses
    #   assuming N and p constant
    #   update counters accordingly
    def F_2num_DIV_remain(self, rows, numerator_add, divisor_add, out_add, remain_add, n=-1, res_n=-1, p=-1, res_p=-1):
        # check n and res_n since we need them in this function:
        if n < 0: n = self.N_bit
        if res_n < 0: res_n = self.N_bit

        # allocate memory for the result:
        for row in rows:
            self.F_write_CMPLX_num(row, out_add, [0,0], n=res_n) # for result
            self.F_write_CMPLX_num(row, out_add + 2*res_n, [0, 0], n=res_n) # for remain

        # define indexes:
        mid_numerator_add = len(self.MAGIC[rows[0]])
        mid_divisor_add = mid_numerator_add + 2*res_n
        conjugate_add = mid_divisor_add +2*res_n

        # initiating mid result memristors:
        self.C_cycles += 1

        # calculate the conjugate of the divisor and write it to the memory:
        # real part - copy (2 times NOT):
        MAGIC.F_1num_NOT(self, rows, divisor_add, mid_numerator_add, n)
        MAGIC.F_1num_NOT(self, rows, mid_numerator_add, conjugate_add, n)


        # imaginary part - invert, then FA with 0 and carry_in = 1, the 0 is
        # from the allocated memory that initialised to 0's:
        MAGIC.F_1num_NOT(self, rows, divisor_add + n, mid_divisor_add, n)

        MAGIC.F_ADD1bit(self, rows, mid_divisor_add, 1, conjugate_add + n, n=n)


        # calculating the multiplication of the divisor and the numerator with
        #  the complex conjugate of the divisor:
        self.C_cycles += 1
        self.F_2num_MUL(rows, numerator_add, conjugate_add, mid_numerator_add, n, res_n, p, res_p)
        self.F_2num_MUL(rows, divisor_add, conjugate_add, mid_divisor_add, n, res_n, p, res_p)

        #free conjugate memory:
        for j in rows:
            self.MAGIC[j].free(2*n)


        # divide separately the real part and the imaginary part by the square
        # abstract value of the divisor (which it's imaginary part is 0):
        MAGIC.F_2num_DIV_remain(self, rows, mid_numerator_add, mid_divisor_add, out_add, remain_add)
        MAGIC.F_2num_DIV_remain(self, rows, mid_numerator_add + res_n, mid_divisor_add, out_add + res_n, remain_add + res_n)

        # free the unnecessary memory:
        for j in rows:
            self.MAGIC[j].free(4*res_n)
        MAGIC.F_update_counters(self)

    # end of function F_2num_DIV_remain
    ##################################################

    ##################################################
    # function name: F_2num_DIV_approx
    # inputs:
    #   rows          - vector with row numbers to execute MUL on
    #   numerator_add - address of numerator msb
    #   divisor_add   - address of divisor msb
    #   out_add       - address of result msb
    #   remain_add    - address of remain msb
    #   n             - the number of bits representing each Re/Im number of the inputs
    #   res_n         - the number of bits representing each Re/Im number of the output
    #   p             - the number of bits representing each Re/Im number FIP of the inputs
    #   res_p         - the number of bits representing each Re/Im number FIP of the output
    # description:
    #   executing fixed point division on two inputs on all given rows.
    #   dividing numerator with divisor
    #   result and remain will be written to given addresses
    #   assuming N and p constant
    #   update counters accordingly
    def F_2num_DIV_approx(self, rows, numerator_add, divisor_add, out_add, n=-1, res_n=-1, p=-1, res_p=-1):

        # check n and res_n since we need them in this function:
        if n < 0: n = self.N_bit
        if res_n < 0: res_n = self.N_bit

        # allocate memory for the result:
        for row in rows:
            self.F_write_CMPLX_num(row, out_add, [0, 0], n=res_n)

        # define indexes:
        mid_numerator_add = len(self.MAGIC[rows[0]])
        mid_divisor_add = mid_numerator_add + 2 * res_n
        conjugate_add = mid_divisor_add + 2 * res_n

        # initiating mid result memristors:
        self.C_cycles += 1

        # calculate the conjugate of the divisor and write it to the memory:
        # real part - copy (2 times NOT):
        MAGIC.F_1num_NOT(self, rows, divisor_add, mid_numerator_add, n)
        MAGIC.F_1num_NOT(self, rows, mid_numerator_add, conjugate_add, n)


        # imaginary part - invert, then FA with 0 and carry_in = 1, the 0 is
        # from the allocated memory that initialised to 0's:
        MAGIC.F_1num_NOT(self, rows, divisor_add + n, mid_divisor_add, n)

        MAGIC.F_ADD1bit(self, rows, mid_divisor_add, 1, conjugate_add + n, n=n)


        # calculating the multiplication of the divisor and the numerator with
        #  the complex conjugate of the divisor:
        self.C_cycles += 1
        self.F_2num_MUL(rows, numerator_add, conjugate_add, mid_numerator_add, n, res_n, p, res_p)
        self.F_2num_MUL(rows, divisor_add, conjugate_add, mid_divisor_add, n, res_n, p, res_p)

        # free conjugate memory:
        for j in rows:
            self.MAGIC[j].free(2 * n)

        # divide separately the real part and the imaginary part by the
        # square
        # abstract value of the divisor (which it's imaginary part is 0):
        MAGIC.F_2num_DIV_approx(self, rows, mid_numerator_add, mid_divisor_add, out_add, res_n, res_p)
        MAGIC.F_2num_DIV_approx(self, rows, mid_numerator_add + res_n, mid_divisor_add, out_add + res_n, res_n, res_p)


        # free the unnecessary memory:
        for j in rows:
            self.MAGIC[j].free(4*res_n)
        MAGIC.F_update_counters(self)

    # end of function F_2num_DIV_approx
    ##################################################