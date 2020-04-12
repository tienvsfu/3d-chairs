import cv2
import os
import numpy as np
from projector import ObjProjector

'''
load chair dataset. Dimension refers to the target dimension of the output image, used to save up memory.
The images are originally 224 x 224.

There are opportunities to improve the dataset by performing image operations to augment the dataset and generating
more negative samples based on the given meshes.
'''

def _generate_positive_data(dimension, obj_dir):
    length = len(os.listdir(obj_dir))
    
    imagesTop = []
    imagesLeftSide = []
    imagesRightSide = []
    imagesFront = []

    pj = ObjProjector(obj_dir)

    for filename in os.listdir(obj_dir):
        front, top, left, right = pj.(dimension, filename)
        imagesFront.append(front)
        imagesTop.append(top)
        imagesLeftSide.append(left)
        imagesRightSide.append(right)

    y_vec_front = np.ones((length), dtype=np.int)
    y_vec_top = np.ones((length), dtype=np.int)
    y_vec_left_side = np.ones((length), dtype=np.int)
    y_vec_right_side = np.ones((length), dtype=np.int)
    

    return imagesFront, imagesTop, imagesLeftSide, imagesRightSide, y_vec_front, y_vec_top, y_vec_left_side, y_vec_right_side

def _generate_negative_data(dimension, obj_dir, part_dir):
    imagesTop = []
    imagesLeftSide = []
    imagesRightSide = []
    imagesFront = []

    y_vec_top = []
    y_vec_left_side = []
    y_vec_right_side = []
    y_vec_front = []



# def load(dimension):

#     imagesTop = []
#     imagesSide = []
#     imagesFront = []
#     isPositive = False

#     ls = 0

#     for id, folder in enumerate(["chairs-data/positive/", "chairs-data/negative/"]):
#         isPositive = not isPositive

#         length = len(os.listdir(folder)) // 3
#         ls += length

#         for filename in os.listdir(folder):

#             view = int(filename.split(".")[0])
#             view = view % 3
#             img = cv2.imread(folder+filename)
#             if dimension < 224:
#                 img = cv2.resize(img, dsize=(dimension, dimension), interpolation=cv2.INTER_CUBIC)
#             img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             img = np.nan_to_num(img)

#             if img is not None:
#                 if view == 2:
#                     imagesSide.append(1. - img / 255.)
#                 elif view == 0:
#                     imagesTop.append(1. - img / 255.)
#                 else:
#                     imagesFront.append(1. - img / 255.)

#         if isPositive:
#             y_vec_top = np.ones((length), dtype=np.int)
#             y_vec_side = np.ones((length), dtype=np.int)
#             y_vec_front = np.ones((length), dtype=np.int)
#         else:
#             y_vec_top = np.append(y_vec_top, np.zeros((length), dtype=np.int), axis=0 )
#             y_vec_side = np.append(y_vec_side, np.zeros((length), dtype=np.int), axis=0 )
#             y_vec_front = np.append(y_vec_front, np.zeros((length), dtype=np.int), axis=0 )

#     imagesTop = np.array(imagesTop)
#     imagesFront = np.array(imagesFront)
#     imagesSide = np.array(imagesSide)

#     #flatten the images
#     imagesTop = np.reshape(imagesTop, (ls, dimension * dimension))
#     imagesFront = np.reshape(imagesFront, (ls, dimension * dimension))
#     imagesSide = np.reshape(imagesSide, (ls, dimension * dimension))

#     seed = 547
#     np.random.seed(seed)
#     np.random.shuffle(imagesTop)
#     np.random.seed(seed)
#     np.random.shuffle(imagesFront)
#     np.random.seed(seed)
#     np.random.shuffle(imagesSide)

#     np.random.seed(seed)
#     np.random.shuffle(y_vec_top)
#     np.random.seed(seed)
#     np.random.shuffle(y_vec_front)
#     np.random.seed(seed)
#     np.random.shuffle(y_vec_side)

#     return imagesTop, imagesFront, imagesSide, y_vec_top, y_vec_front, y_vec_side


# def runtime_load_test():
#     import time
#     start_time = time.time()
#     imagesTop, imagesFront, imagesSide, y_vec_top, y_vec_front, y_vec_side = load(56)
#     print("--- %s min ---" % ((time.time() - start_time) /  60))
#     #print(imagesTop.shape[0])

