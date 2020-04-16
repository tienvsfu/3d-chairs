import numpy as np
import tensorflow.compat.v1 as tf
import os
from PIL import Image
import trimesh
import operator

from .model import cnn_model_fn
from .projector import ObjProjector

tf.logging.set_verbosity(tf.logging.INFO)

# obj_dir = os.path.join('..','data','mm-a')

# score_dir = os.path.join('scores.txt')

# dimension = 56

# project_size = 800

def resize(array, size):
    return np.array(Image.fromarray(array).resize((size, size)))

def load(obj_dir,  batch_size=20, dimension=56, project_size=800):
    
    images_front = []
    images_top = []
    images_left = []
    images_right = []

    obj_meshes = []

    pj = ObjProjector()

    files = os.listdir(obj_dir)
    counter = 0
    for filename in files:
        obj_mesh = trimesh.load(os.path.join(obj_dir, filename))
        obj_meshes.append(obj_mesh)

        if counter == batch_size-1 or filename == files[len(files) - 1]:
            for obj_mesh in obj_meshes:
                front, top, left, right = pj.project(project_size, obj_mesh)

                if (dimension < project_size):
                    front = resize(front, dimension)
                    top = resize(top, dimension)
                    left = resize(left, dimension)
                    right = resize(right, dimension)
            
                images_front.append(front)
                images_top.append(top)
                images_left.append(left)
                images_right.append(right)

            obj_meshes = []
            counter = 0
        else:
            counter = counter + 1
    
    ls = len(images_front)

    images_front = np.array(images_front)
    images_top = np.array(images_top)
    images_left = np.array(images_left)
    images_right = np.array(images_right)
        
        #flatten images
    images_top = np.reshape(images_top, (ls, dimension * dimension))
    images_front = np.reshape(images_front, (ls, dimension * dimension))
    images_left = np.reshape(images_left, (ls, dimension * dimension))
    images_right = np.reshape(images_right, (ls, dimension * dimension))

    return files, images_top, images_front, images_left, images_right


def evaluate(obj_dir,  batch_size=20, dimension=56, project_size=800):
    model_output_dir = os.path.join(os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))), 'checkpoint')

    files, images_top, images_front, images_left, images_right = load(obj_dir)

    test_images = {}
    
    test_images["Top"] = images_top
    test_images["Front"] = images_front
    test_images["Left"] = images_left
    test_images["Right"] = images_right

    test_evaluations = [[],[],[],[]]

    for id, view in enumerate(["Top","Front","Left", "Right"]):
            model_dir = os.path.join(model_output_dir, view)
            classifier = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir=model_dir, params={'dimension': dimension})

            eval_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": test_images[view]},
                                                            num_epochs=1,
                                                            shuffle=False)

            eval_results = classifier.predict(input_fn=eval_input_fn)

            for eval in eval_results:
                test_evaluations[id].append(eval['probabilities'][1])


    evaluation_chairs = np.amin(test_evaluations, axis=0)

    results = {}
    for i, filename in enumerate(files):
        key = filename.split(".")[0]
        val = evaluation_chairs[i]
        results.update( {key : val} )

    sorted_results = dict(sorted(results.items(), key=operator.itemgetter(1),reverse=True))

    print("Sorted plausible scores of models: ")
    print(sorted_results)

    return sorted_results

#Write results to file 
def export_results(sorted_results, score_dir):
    #print results to txt file
    output_file = open(score_dir, 'w+')
    for key in sorted_results:
        output_file.write('obj ' + str(key) + ': ' + str(sorted_results[key]) + '\n')
    output_file.close()
