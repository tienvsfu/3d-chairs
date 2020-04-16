import os
import ntpath
import sys
import shutil
import params
from scorer import evaluate

def score():
    obj_dirs = params.obj_dirs
    score_dir = params.score_dir

    scorer
    results is a dict with structure: {'mm_a':{0 : probability_0, 1:probability_1}, 'mm_b':{0: probability_0, 1: probability_1}}
    results = {}
    for obj_dir in obj_dirs:
        base_name =  os.path.basename(os.path.normpath(obj_dir))
        sorted_result = evaluate.evaluate(obj_dir)
        results[base_name] = sorted_result

    #Write to txt file
    if os.path.exists(score_dir):
        shutil.rmtree(score_dir)

    os.mkdir(score_dir)

    for base_name in results:
        print(base_name)
        score_file_dir = os.path.join(score_dir, base_name + '.txt')
        evaluate.export_results(results[base_name], score_file_dir)
