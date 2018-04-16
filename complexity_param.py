######## COMPLEXITY PARAMETERS ########

# use this file to change the amount of cycles or memristors usage
# of the different functions according to the algorithm that being simulated.

# MEMORY USAGE:
# parameter       --------     function

# F_2num_FA():
mem_FA = lambda n:             5

# F_ADD1():
mem_ADD1bit = lambda n:           5

# F_2num_MUL():
mem_MUL = lambda n:            20*n-5


# CYCLES:
# parameter       --------     function

# F_2num_FA():
cycle_FA = lambda n:           15*n

# F_ADD1():
cycle_ADD1bit = lambda n:         7*n

# F_2num_MUL():
cycle_MUL = lambda n:          13*n**2-14*n+6