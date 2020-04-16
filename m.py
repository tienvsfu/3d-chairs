

import re

from p import *
from mm import *
from s import *

# load
c1 = input("Please enter test IDs (e.g. 2585, 2323, 43872):\n")
selected_test_cases = re.findall('\d+', c1)
c2 = []
for test_case in selected_test_cases:
    c2.append(int(test_case))

parse(c1)
generate(10,c2)
score()

# display
ranking = []
f = open('scores/mm-a.txt')
for l in f:
    ob = re.findall('\d+', l)
    ranking.append(int(ob[0]))

display(ranking[0:6])