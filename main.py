import argparse
import os
import shutil

from scorer import evaluate
from gen_chairs import gen_chairs, display

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--input-path', help='Path to folder with part jsons', default='./data/in')
    parser.add_argument('-m','--parts-output-path', help='Path to output corresponding .objs', default='./data/out')
    parser.add_argument('-o','--output-path', help='Path to put full generated chairs', default='./data/mm')

    args = parser.parse_args()

    in_path = args.input_path
    parsed_chairs_path = args.parts_output_path
    generated_chairs_path = args.output_path

    # convert .jsons into part .objs
    from convert_input import *
    parse(in_path, parsed_chairs_path)

    # generate some chairs, and export as .objs to generated_chairs_path
    gen_chairs(path_to_chairs=parsed_chairs_path, path_to_output=generated_chairs_path, n_times=10)

    # sanity check
    chair_meshes = []
    chair_dirs = os.listdir(generated_chairs_path)

    for chair_dir in chair_dirs:
        try:
            chair_mesh = trimesh.load(os.path.join(generated_chairs_path, chair_dir))
        except:
            print(f'{chair_dir} was fuct')
            exit()

    # calculate the scores for the generated chairs
    sorted_results = evaluate.evaluate(generated_chairs_path)
    print(sorted_results)

    score_dir = os.path.join(generated_chairs_path, 'scores.txt')
    if os.path.exists(score_dir):
        os.remove(score_dir)
    evaluate.export_results(sorted_results, score_dir)

    # sorted_results = score()

    # display
    # ranking = []
    # for key in sorted_results:
    #     ranking.append(int(key))
    # display(ranking[0:6])

    # display(list(map(int, sorted_results.keys()))[0:6])
