import os
import shutil
from scorer import evaluate

import re

from p import *
from mm import *

obj_dir = os.path.join('.','data', 'mm')

score_dir = os.path.join('.', 'score')

def score():
    sorted_results = evaluate.evaluate(obj_dir)
    
    if not os.path.exists(score_dir):
        os.mkdir(score_dir)
    score_file_dir = os.path.join(score_dir, 'scores.txt')
    if os.path.exists(score_file_dir):
        os.remove(score_file_dir)
    evaluate.export_results(sorted_results, score_file_dir)
    
    return sorted_results


# load
c1 = input("Please enter test IDs (e.g. 2585, 2323, 43872):\n")
selected_test_cases = re.findall('\d+', c1)
c2 = []
for test_case in selected_test_cases:
    c2.append(int(test_case))

parse(c1)
generate(10,c2)

sorted_results = score()

# display
# ranking = []
# for key in sorted_results:
#     ranking.append(int(key))
# display(ranking[0:6])

display(list(map(int, sorted_results.keys()))[0:6])
