# import os
# import ntpath
# import sys
# import shutil
# import params
# from scorer import evaluate
# obj_dirs = params.obj_dirs
# score_dir = params.score_dir

import re

from p import *
from mm import *

# load
c1 = input("Please enter test IDs (e.g. 2585, 2323, 43872):\n")
selected_test_cases = re.findall('\d+', c1)
c2 = []
for test_case in selected_test_cases:
    c2.append(int(test_case))

# print(c2)
# set = 'b'

# if set=='a':
#     c1 = "2585, 2323, 43872"
#     c2 = [2585, 2323, 43872]
# elif set=='b':
#     c1 = "39055, 37529, 40096, 41975, 37546"
#     c2 = [39055, 37529, 40096, 41975, 37546]
# elif set=='c':
#     c1 = "37107, 39781, 40141, 39426, 35698, 2320, 40546, 37790, 43006, 37108"
#     c2 = [37107, 39781, 40141, 39426, 35698, 2320, 40546, 37790, 43006, 37108]
# else:
#     print('no such set')
#     exit() 

parse(c1)
generate(10,c2)

# scorer
#results is a dict with structure: {'mm_a':{0 : probability_0, 1:probability_1}, 'mm_b':{0: probability_0, 1: probability_1}}
# results = {}
# for obj_dir in obj_dirs:
#     base_name =  os.path.basename(os.path.normpath(obj_dir))
#     sorted_result = evaluate.evaluate(obj_dir)
#     results[base_name] = sorted_result

# #Write to txt file
# if os.path.exists(score_dir):
#     shutil.rmtree(score_dir)

# os.mkdir(score_dir)

# for base_name in results:
#     print(base_name)
#     score_file_dir = os.path.join(score_dir, base_name + '.txt')
#     evaluate.export_results(results[base_name], score_file_dir)


# display
ranking = []
f = open('scores/mm-a.txt')
for l in f:
    ob = re.findall('\d+', l)
    ranking.append(int(ob[0]))

display(ranking[0:6])