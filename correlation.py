"""
Pearson Rho, Spearman Rho, and Kendall Tau

Correlation algorithms

Drew J. Nase

Expects path to a file containing data series - 
one per line, separated by one or more spaces.
"""

import math
import sys
import string
from itertools import combinations

if len(sys.argv) > 1:
    #data file given as arg
    filename = sys.argv[1]
else:
    sys.exit("Usage: python " + sys.argv[0] + " [matrix filename]")

x = []
y = []

def split_values(v):
	buff = map(string.strip, string.split(v, " "))
	x.append(int(buff[0]))
	y.append(int(buff[1]))

#x, y must be one-dimensional arrays of the same length

#Pearson algorithm
def pearson(x, y):
    assert len(x) == len(y) > 0
    q = lambda n: len(n) * sum(map(lambda i: i ** 2, n)) - (sum(n) ** 2)
    return (len(x) * sum(map(lambda a: a[0] * a[1], zip(x, y))) - sum(x) * sum(y)) / math.sqrt(q(x) * q(y))

#Spearman algorithm
def spearman(x, y):
    assert len(x) == len(y) > 0
    q = lambda n: map(lambda val: sorted(n).index(val) + 1, n)
    d = sum(map(lambda x, y: (x - y) ** 2, q(x), q(y)))
    return 1.0 - 6.0 * d / float(len(x) * (len(y) ** 2 - 1.0))

#Kendall algorithm
def kendall(x, y):
    assert len(x) == len(y) > 0
    c = 0 #concordant count
    d = 0 #discordant count
    t = 0 #tied count
    for (i, j) in combinations(xrange(len(x)), 2):
        s = (x[i] - x[j]) * (y[i] - y[j])
        if s:
            c += 1
            d += 1
            if s > 0:
                t += 1
            elif s < 0:
                t -= 1
        else:
            if x[i] - x[j]:
                c += 1
            elif y[i] - y[j]:
                d += 1
    return t / math.sqrt(c * d)

#read in file
with open(filename) as f:
	map(split_values, f.readlines())

print 'Pearson Rho: %f' % pearson(x, y)

print 'Spearman Rho: %f' % spearman(x, y)

print 'Kendall Tau: %f' % kendall(x, y)
