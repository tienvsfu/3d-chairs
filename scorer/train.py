import numpy as np
import tensorflow.compat.v1 as tf
from chair_dataset import ChairDataset
import model
import trimesh
import os
import time

OBJ_DIR = os.path.join('..', '..', 'Chair', 'models')

PART_DIR = os.path.join('..', '..', 'Chair_parts')

MODEL_OUTPUT_DIR = os.path.join('checkpoint')

DIMENSION = 56

def is_obj_file(filepath):
    return filepath.endswith('.obj')

def load(batch_size=20):
    cd = ChairDataset(800)
    
    image_top_ls = []
    image_front_ls = []
    image_left_ls = []
    image_right_ls = []

    label_top_ls = []
    label_front_ls = []
    label_left_ls = []
    label_right_ls = []

    images = []
    labels = []
    obj_meshes = []
    part_meshes = []
    counter = 0
    files = os.listdir(OBJ_DIR)
    part_dirs = os.listdir(PART_DIR)
    for i in range(len(files)):
        file = files[i]
        obj_mesh = trimesh.load(os.path.join(OBJ_DIR, file))
        obj_meshes.append(obj_mesh)

        d = part_dirs[i]
        obj_part_dir = os.path.join(PART_DIR, d, 'objs')
        obj_files = [os.path.join(obj_part_dir, f) for f in os.listdir(obj_part_dir) if is_obj_file(f)]
        part_mesh = [trimesh.load(f) for f in obj_files]
        part_meshes.append(part_mesh)
        # if (i == 50):
        #     break
        if counter == batch_size-1:
           
            imagesTop, imagesFront, imagesLeft, imagesRight, labelsTop, labelsFront, labelsLeft, labelsRight = cd.generate_data(DIMENSION, obj_meshes, part_meshes)
            
            image_top_ls.extend(imagesTop)
            image_front_ls.extend(imagesFront)
            image_left_ls.extend(imagesLeft)
            image_right_ls.extend(imagesRight)

            label_top_ls.extend(labelsTop)
            label_front_ls.extend(labelsFront)
            label_left_ls.extend(labelsLeft)
            label_right_ls.extend(labelsRight)

            print('Loaded ' + str(len(image_top_ls)/2))

            obj_meshes = []
            part_meshes = []
            counter = 0
        else:
            counter = counter + 1

    images.append(np.array(image_top_ls))
    images.append(np.array(image_front_ls))
    images.append(np.array(image_left_ls))
    images.append(np.array(image_right_ls))

    labels.append(np.array(label_top_ls))
    labels.append(np.array(label_front_ls))
    labels.append(np.array(label_left_ls))
    labels.append(np.array(label_right_ls))

    return images, labels

print('Load & generate projection data..')
start_time = time.time()
images, labels = load()
print('Preparing data elapsed time: ' + str(time.time() - start_time) + ' seconds\n')


print('NN Training data..')
start_time = time.time()
model.train(DIMENSION, images, labels, MODEL_OUTPUT_DIR)
print('Training data elapsed time: ' + str(time.time() - start_time) + ' seconds\n')