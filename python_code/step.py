import numpy as np
import random
from step_utils import dec2bin
from step_utils import bin2dec
from step_utils import adder
from step_utils import multiplier
from step_utils import division

N = random.randint(1, 50)                                   # size of vector from 1 to 50
print("N = ", N)

Hinit = random.random() + random.randint(0, 1)              # initial step from 0 to 2
Hinit = dec2bin(str(Hinit), 7)                               # approximate to match fixed point representation
print("Initial h = ", bin2dec(Hinit))

L = 2.0                                                       # tolerance
print("Tolerance = ", L)

X0 = []
X1 = []
Hnew = 0

for i in range(N):
    num = random.random() + random.randint(0, 60)       # random decimal number between 0 and 60.99
    sf = random.randint(0, 5)                           # random scale factor
    strBinNum = dec2bin(str(num), sf)                   # 16 bit binary string
    X0.append(strBinNum)

    num = random.random() + random.randint(0, 60)      # random decimal number between 0 and 60.99
    sf = random.randint(0, 5)                          # random scale factor
    strBinNum = dec2bin(str(num), sf)                  # 16 bit binary string
    X1.append(strBinNum)

print("X0 in bin : ", X0)

print("X0 in dec : ")
for i in range(N):
    print(bin2dec(X0[i]))

print("X1 in bin : ", X1)

print("X1 in dec : ")
for i in range(N):
    print(bin2dec(X1[i]))

error = "0000000000000000"
for i in range(N):
    diff = adder(X0[i], X1[i], 1, 0)          # Diff using subtract module
    sf_diff = diff >> 13                            # store scale factor of diff to convert it from dec to binary
    diff = bin(diff).split('b')[1]                  # Diff in fixed point as binary
    diff = bin2dec(diff)                            # get decimal value of difference
    diff = np.abs(diff)                             # get absolute value
    diff = dec2bin(str(diff), sf_diff)              # change to binary string again
    error = bin(adder(error, diff, 0, 0)).split('b')[1]

print("Error in binary = ", error)
print("Error in decimal = ", bin2dec(error))

if bin2dec(error) > L:
    const = dec2bin(str(0.9), 7)                                # let the scale factor be 3, it can be changed
    Hinit2 = bin(multiplier(Hinit, Hinit)).split('b')[1]        # Hinit squared in binary fixed point representation
    Hnew = bin(multiplier(const, Hinit2)).split('b')[1]         # Hinit square * 0.9
    Hnew = bin(multiplier(Hnew, dec2bin(str(L), 3))).split('b')[1]
    Hnew = bin(division(1, Hnew, error))                     # scale factor of error assume 3 can be changed

    print("Hnew in binary = ", Hnew)                            # cause error sometimes depending on error value
    print("Hnew in decimal = ", bin2dec(Hnew))

    #Hnew = (0.9 * pow(Hinit, 2) * L) / error
