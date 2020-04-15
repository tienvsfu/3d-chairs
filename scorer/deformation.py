import os
import functools
import math
import numpy as np
import pyrender
import trimesh
import matplotlib.pyplot as plt
import random
from enum import Enum
from numpy import linalg as LA
from pyrender.constants import RenderFlags as RF

class DeformStrategy(Enum):
    REMOVE = 1
    ROTATE = 2
    SCALE = 3
    TRANSLATE = 4
    NOTHING = 5
    DUPLICATE = 6

class ChairDeformator:
    def __init__(self, part_meshes):
        self.part_meshes = [m.copy() for m in part_meshes]
        random.seed(0)

    def _merge_meshes(self, meshes):
        return functools.reduce(lambda m1, m2: trimesh.util.concatenate(m1, m2), meshes)        
        
    def _choose_strategy(self):
        return random.choice(list(DeformStrategy))
    
    def _rotate(self, mesh):
        # TODO: rotate at random angle
        angle = random.uniform(0.0, 360.0)
        axis_idx = random.randint(0,2)
        mesh.apply_transform(self._rotate_matrix(angle, axis=axis_idx))
        return mesh

    def _scale(self, mesh):
        # TODO: resize at random scale
        sx = random.uniform(0.0, 1.5)
        sy = random.uniform(0.0, 1.5)
        sz = random.uniform(0.0, 1.5)
        mesh.apply_transform(self._scale_matrix(sx, sy, sz))
        return mesh

    def _translate(self, mesh):
        # TODO: move randomly
        x_extent, y_extent, z_extent = mesh.scene().extents
        tx = random.uniform(0.0, 1.5)*x_extent
        ty = random.uniform (0.0, 1.5)*y_extent
        tz = random.uniform(0.0, 1.5)*z_extent
        mesh.apply_transform(self._translate_matrix(tx, ty, tz))
        return mesh
    
    def _duplicate(self, mesh):
        mesh_dup = mesh.copy()
        return self._translate(mesh_dup)
    
    def _rotate_matrix(self, angle, axis=0):
        s = math.sin(angle)
        c = math.cos(angle)
        rx_matrix = np.array([[1,0,0,0], [0,c,-s,0], [0,s,c,0], [0,0,0,1]])
        ry_matrix = np.array([[c,0,s,0], [0,1,0,0], [-s,0,c,0], [0,0,0,1]])
        rz_matrix = np.array([[c,-s,0,0], [s,c,0,0], [0,0,1,0], [0,0,0,1]])
        if (axis == 0):
            return rx_matrix
        elif (axis == 1):
            return ry_matrix
        elif (axis == 2):
            return rz_matrix
    
    def _translate_matrix(self, tx, ty, tz):
        return np.array([[1,0,0,tx], [0,1,0,ty], [0,0,1,tz], [0,0,0,1]])
    
    def _scale_matrix(self, sx, sy, sz):
        return np.array([[sx,0,0,0], [0,sy,0,0], [0,0,sz,0], [0,0,0,1]])

    def deform(self):
        final_meshes = []

        for mesh in self.part_meshes:
            strategy = self._choose_strategy()
            if (strategy == DeformStrategy.NOTHING):
                final_meshes.append(mesh)
            elif (strategy == DeformStrategy.REMOVE):
                continue
            elif (strategy == DeformStrategy.ROTATE):
                final_meshes.append(self._rotate(mesh))
            elif (strategy == DeformStrategy.SCALE):
                final_meshes.append(self._scale(mesh))
            elif (strategy == DeformStrategy.TRANSLATE):
                final_meshes.append(self._translate(mesh))
            elif (strategy == DeformStrategy.DUPLICATE):
                final_meshes.append(self._duplicate(mesh))

        return self._merge_meshes(final_meshes)

# def is_obj_file(filepath):
#     return filepath.endswith('.obj')

# obj_dir = os.path.join('..', '..', 'Chair_parts', '173', 'objs')
# obj_files = [os.path.join(obj_dir, f) for f in os.listdir(obj_dir) if is_obj_file(f)]

# meshes = [trimesh.load(f) for f in obj_files]

# deformator = ChairDeformator(meshes)
# deformed_chair = deformator.deform()
# deformed_chair.scene().show()