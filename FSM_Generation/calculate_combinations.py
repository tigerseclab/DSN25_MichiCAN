# find the number of different ways we can choose any number of elements from 2047 possible CAN IDs

from math import comb

total = 0
for i in range(1, 2048):
    total += comb(2047, i)
print(total)
