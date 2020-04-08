#!/usr/bin/python3
__version__ = '0.0.1' # Time-stamp: <2019-05-30T13:51:53Z>
## Language: Japanese/UTF-8

"""Experiment"""

##
## License:
##
##   Public Domain
##   (Since this small code is close to be mathematically trivial.)
##
## Author:
##
##   JRF
##   http://jrf.cocolog-nifty.com/software/
##   (The page is written in Japanese.)
##

import math
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--trials", default=1000, dest="trials", type=int)
parser.add_argument("--n", default=1000, dest="n", type=int)
parser.add_argument("--upper", default=300, dest="upper", type=int)
parser.add_argument("--a", default=0.3, dest="a", type=float)
parser.add_argument("--b", default=1.0, dest="b", type=float)

args = parser.parse_args()
TRIALS = args.trials
N = args.n
UPPER = args.upper
A = args.a / N
B = args.b

num_0 = 0
num_999 = 0
num_500 = 0
for i in range(TRIALS):
#    if i % 100 == 0:
#        print(i, flush=True)
    l = [(random.uniform(0.0, A * j + B), j) for j in range(N)]
    l = sorted(l, key=lambda x: x[0], reverse=True)
    for j in range(UPPER):
        if l[j][1] == 0:
            num_0 += 1
        if l[j][1] == N - 1:
            num_999 += 1
        if l[j][1] == N // 2:
            num_500 += 1

print("%g %g %g" % (float(num_0 / TRIALS), float(num_500 / TRIALS),
                    float(num_999 / TRIALS)))

