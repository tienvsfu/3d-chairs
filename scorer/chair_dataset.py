import cv2
import os
import numpy as np
from projector import ObjProjector
from deformation import ChairDeformator
import trimesh
import matplotlib.pyplot as plt
from PIL import Image


'''
load chair dataset. Dimension refers to the target dimension of the output image, used to save up memory.
The images are originally 224 x 224.

There are opportunities to improve the dataset by performing image operations to augment the dataset and generating
more negative samples based on the given meshes.
'''

class ChairDataset:
    def __init__(self, project_size):
        self.project_size = project_size

    def _resize(self, array, size):
        return np.array(Image.fromarray(array).resize((size, size)))

    def _generate_positive_data(self, dimension, obj_meshes):
        length = len(obj_meshes)
        
        images_top = []
        images_left_side = []
        images_right_side = []
        images_front = []

        pj = ObjProjector()

        for obj_mesh in obj_meshes:
            front, top, left, right = pj.project(self.project_size, obj_mesh)

            if (dimension < self.project_size):
                front = self._resize(front, dimension)
                top = self._resize(top, dimension)
                left = self._resize(left, dimension)
                right = self._resize(right, dimension)
            
            images_front.append(front)
            images_top.append(top)
            images_left_side.append(left)
            images_right_side.append(right)

        y_vec_front = np.ones((length), dtype=np.int)
        y_vec_top = np.ones((length), dtype=np.int)
        y_vec_left_side = np.ones((length), dtype=np.int)
        y_vec_right_side = np.ones((length), dtype=np.int)
        

        return images_front, images_top, images_left_side, images_right_side, y_vec_front, y_vec_top, y_vec_left_side, y_vec_right_side

    def _generate_negative_data(self, dimension, part_meshes):
        images_top = []
        images_left_side = []
        images_right_side = []
        images_front = []

        y_vec_top = []
        y_vec_left_side = []
        y_vec_right_side = []
        y_vec_front = []

        pj = ObjProjector()

        for part_mesh in part_meshes:
            df = ChairDeformator(part_mesh)
            deformed_obj_mesh = df.deform()
            front, top, left, right = pj.project(self.project_size, deformed_obj_mesh)

            if (dimension < self.project_size):
                front = self._resize(front, dimension)
                top = self._resize(top, dimension)
                left = self._resize(left, dimension)
                right = self._resize(right, dimension)

            images_front.append(front)
            images_top.append(top)
            images_left_side.append(left)
            images_right_side.append(right)
        
        length = len(images_top)

        y_vec_front = np.zeros((length), dtype=np.int)
        y_vec_top = np.zeros((length), dtype=np.int)
        y_vec_left_side = np.zeros((length), dtype=np.int)
        y_vec_right_side = np.zeros((length), dtype=np.int)

        return images_front, images_top, images_left_side, images_right_side, y_vec_front, y_vec_top, y_vec_left_side, y_vec_right_side


    def generate_data(self, dimension, obj_meshes, part_meshes):
        images_top = []
        images_left = []
        images_right = []
        images_front = []
        

        pos_front, pos_top, pos_left, pos_right, y_pos_front, y_pos_top, y_pos_left, y_pos_right = self._generate_positive_data(dimension, obj_meshes)

        neg_front, neg_top, neg_left, neg_right, y_neg_front, y_neg_top, y_neg_left, y_neg_right = self._generate_negative_data(dimension, part_meshes)

        images_front.extend(pos_front)
        images_front.extend(neg_front)
    
        images_top.extend(pos_top)
        images_top.extend(neg_top)
        
        images_left.extend(pos_left)
        images_left.extend(neg_left)
        
        images_right.extend(pos_right)
        images_right.extend(neg_right)

        y_vec_front = np.append(y_pos_front, y_neg_front)
        y_vec_top = np.append(y_pos_top, y_neg_top)
        y_vec_left = np.append(y_pos_left, y_neg_left)
        y_vec_right = np.append(y_pos_right, y_neg_right)

        ls = y_vec_front.shape[0]

        images_front = np.array(images_front)
        images_top = np.array(images_top)
        images_left = np.array(images_left)
        images_right = np.array(images_right)
        
        #flatten images
        images_top = np.reshape(images_top, (ls, dimension * dimension))
        images_front = np.reshape(images_front, (ls, dimension * dimension))
        images_left = np.reshape(images_left, (ls, dimension * dimension))
        images_right = np.reshape(images_right, (ls, dimension*dimension))

        seed = 547
        np.random.seed(seed)
        np.random.shuffle(images_top)
        np.random.seed(seed)
        np.random.shuffle(images_front)
        np.random.seed(seed)
        np.random.shuffle(images_left)
        np.random.seed(seed)
        np.random.shuffle(images_right)

        np.random.seed(seed)
        np.random.shuffle(y_vec_top)
        np.random.seed(seed)
        np.random.shuffle(y_vec_front)
        np.random.seed(seed)
        np.random.shuffle(y_vec_left)
        np.random.seed(seed)
        np.random.shuffle(y_vec_right)

        return images_top, images_front, images_left, images_right, y_vec_top, y_vec_front, y_vec_left, y_vec_right


# def is_obj_file(filepath):
#     return filepath.endswith('.obj')

# obj_part_dir_1 = os.path.join('..', '..', 'Chair_parts', '172', 'objs')
# obj_files_1 = [os.path.join(obj_part_dir_1, f) for f in os.listdir(obj_part_dir_1) if is_obj_file(f)]

# part_meshes_1 = [trimesh.load(f) for f in obj_files_1]

# obj_part_dir_2 = os.path.join('..', '..', 'Chair_parts', '173', 'objs')
# obj_files_2 = [os.path.join(obj_part_dir_2, f) for f in os.listdir(obj_part_dir_2) if is_obj_file(f)]

# part_meshes_2 = [trimesh.load(f) for f in obj_files_2]

# part_meshes = []
# part_meshes.append(part_meshes_1)
# part_meshes.append(part_meshes_2)

# obj_dir_1 = os.path.join('..', '..', 'Chair', 'models', '172.obj')
# obj_mesh_1 = trimesh.load(obj_dir_1)

# obj_dir_2 = os.path.join('..', '..', 'Chair', 'models', '173.obj')
# obj_mesh_2 = trimesh.load(obj_dir_2)

# obj_meshes = []
# obj_meshes.append(obj_mesh_1)
# obj_meshes.append(obj_mesh_2)

# cd = ChairDataset(800)

# # pos_front, pos_top, pos_left, pos_right, y_pos_front, y_pos_top, y_pos_left, y_pos_right = cd._generate_positive_data(3, obj_meshes)

# # neg_front, neg_top, neg_left, neg_right, y_neg_front, y_neg_top, y_neg_left, y_neg_right = cd._generate_negative_data(3, part_meshes)

# images_front, images_top, images_left_side, images_right_side, y_vec_front, y_vec_top, y_vec_left_side, y_vec_right_side = cd.generate_data(56, obj_meshes, part_meshes)
