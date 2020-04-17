import argparse
import os
import shutil
import pdb

from scorer import evaluate
from gen_chairs import gen_chairs, display

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-path', help='Path to folder with part jsons', default='./data/in')
    parser.add_argument('-id','--chair-ids', help='Chair IDs in input path, or "all"', default='all')

    args = parser.parse_args()

    in_path = args.input_path
    last_dir = in_path.split('/')[-1]

    parsed_chairs_path = os.path.join(in_path, '..', last_dir+'_parse_out')
    generated_chairs_path = os.path.join(in_path, '..', last_dir+'_generated')
    chair_ids = args.chair_ids

    # convert .jsons into part .objs
    from convert_input import *
    parse(in_path, parsed_chairs_path, chair_ids)

    # generate some chairs, and export as .objs to generated_chairs_path
    generated_chairs = gen_chairs(path_to_chairs=parsed_chairs_path,
                                  path_to_output=generated_chairs_path,
                                  chair_ids=chair_ids,
                                  n_times=10)

    # sanity check
    chair_meshes = []
    chair_dirs = os.listdir(generated_chairs_path)

    for chair_dir in chair_dirs:
        extension = os.path.splitext(chair_dir)[1][1:]
        if extension == 'obj':
            try:
                chair_mesh = trimesh.load(os.path.join(generated_chairs_path, chair_dir))
            except:
                print(f'{chair_dir} was fuct. Please feed your pet a banana')
                exit()

    # calculate the scores for the generated chairs
    sorted_results = evaluate.evaluate(generated_chairs_path)
    print(sorted_results)

    score_dir = os.path.join(generated_chairs_path, 'scores.txt')
    if os.path.exists(score_dir):
        os.remove(score_dir)
    evaluate.export_results(sorted_results, score_dir)

    sorted_chairs = [generated_chairs[int(i)] for i in sorted_results.keys()]
    # pdb.set_trace()

    display(sorted_chairs)