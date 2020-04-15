import numpy as np
import tensorflow.compat.v1 as tf
import os
import cv2
from model import cnn_model_fn
from projector import ObjProjector
from PIL import Image
import trimesh
import operator

tf.logging.set_verbosity(tf.logging.INFO)

OBJ_DIR = os.path.join('..', '..','output')

DIMENSION = 56

PROJECT_SIZE = 800

def resize(array, size):
    return np.array(Image.fromarray(array).resize((size, size)))

def load(batch_size=20):
    
    images_front = []
    images_top = []
    images_left = []
    images_right = []

    obj_meshes = []

    pj = ObjProjector()

    files = os.listdir(OBJ_DIR)
    counter = 0
    for filename in files:
        obj_mesh = trimesh.load(os.path.join(OBJ_DIR, filename))
        obj_meshes.append(obj_mesh)

        if counter == batch_size-1 or filename == files[len(files) - 1]:
            for obj_mesh in obj_meshes:
                front, top, left, right = pj.project(PROJECT_SIZE, obj_mesh)

                if (DIMENSION < PROJECT_SIZE):
                    front = resize(front, DIMENSION)
                    top = resize(top, DIMENSION)
                    left = resize(left, DIMENSION)
                    right = resize(right, DIMENSION)
            
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
    images_top = np.reshape(images_top, (ls, DIMENSION * DIMENSION))
    images_front = np.reshape(images_front, (ls, DIMENSION * DIMENSION))
    images_left = np.reshape(images_left, (ls, DIMENSION * DIMENSION))
    images_right = np.reshape(images_right, (ls, DIMENSION * DIMENSION))

    return files, images_top, images_front, images_left, images_right

#####################################

files, images_top, images_front, images_left, images_right = load()

test_images = {}
    #then the rest are test images and labels
test_images["Top"] = images_top
test_images["Front"] = images_front
test_images["Left"] = images_left
test_images["Right"] = images_right

test_evaluations = [[],[],[],[]]

for id, view in enumerate(["Top","Front","Left", "Right"]):
        classifier = tf.estimator.Estimator(model_fn=cnn_model_fn, model_dir="checkpoint/"+view+"/", params={'dimension': DIMENSION})

        eval_input_fn = tf.estimator.inputs.numpy_input_fn(x={"x": test_images[view]},
                                                           num_epochs=1,
                                                           shuffle=False)

        eval_results = classifier.predict(input_fn=eval_input_fn)


        # This is how you extract the correlation to the positive class of the first element in your evaluation folder
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

#print results to txt file
output_file = open('scores.txt', 'w+')
for key in sorted_results:
    output_file.write('Score for output obj ' + str(key) + ' is: ' + str(sorted_results[key]) + '\n')
output_file.close()
