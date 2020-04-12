import numpy as np
import trimesh
import pdb
import os
import random

from math import pi as pi
from trimesh.transformations import scale_matrix, translation_matrix, rotation_matrix
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon

random.seed(2)
MULP = 0.4
shift_X = 2

all_chairs_dir = '../chairs/'
chair_meshes = []

chair_dirs = os.listdir(all_chairs_dir)
chair_meshes = []
DELTA = 0.5

def curve2(mesh):
    max_x = mesh.vertices[:, 0].max()
    min_x = mesh.vertices[:, 0].min()

    mid_x = (max_x + min_x) / 2
    d = np.abs(mid_x - min_x)

    for i in range(len(mesh.vertices)):
        # 1 to 0, 0 to 1
        t = np.abs(mesh.vertices[i][0] - mid_x) / d
        mesh.vertices[i][1] += np.cos(t * pi/2) * MULP

    return mesh

def curve3(mesh):
    max_x = mesh.vertices[:, 0].max()
    min_x = mesh.vertices[:, 0].min()

    mid_x = (max_x + min_x) / 2
    d_half = np.abs(min_x - mid_x)

    left_X = mid_x - DELTA * d_half
    d = np.abs(min_x - left_X)
    right_X = mid_x + DELTA * d_half
    d_mid = np.abs(right_X - left_X)
    Y_line = np.cos(0 * pi/2) * MULP

    for i in range(len(mesh.vertices)):
        x = mesh.vertices[i][0]

        if x < left_X:
            # 1 to 0
            t = np.abs(x - left_X) / d
            mesh.vertices[i][1] += np.cos(t * pi/2) * MULP
        elif x < right_X:
            # 1 to 0, 0 to 1
            t = np.abs(x - mid_x) / d_mid
            mesh.vertices[i][1] += Y_line
        else:
            t = np.abs(x - right_X) / d
            mesh.vertices[i][1] += np.cos(t * pi/2) * MULP

    return mesh

for chair_dir in chair_dirs:
    seat_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'back.obj')
    mesh = trimesh.load(seat_mesh_dir)

    while len(mesh.vertices) < 10000:
        mesh = mesh.subdivide()

    R = rotation_matrix(pi/2, [1, 0, 0])
    mesh = mesh.apply_transform(R)

    mesh = curve3(mesh)

    chair_meshes.append(mesh)

scenes = []
ncols = nrows = int(np.ceil(np.sqrt(len(chair_meshes))))

for i in range(nrows):
    T_x = shift_X * i

    for j in range(ncols):
        index = i * nrows + j

        if index >= len(chair_meshes):
            break

        T_y = shift_X * j
        T = translation_matrix([T_x, T_y, 0])
        
        c = chair_meshes[index]
        c.apply_transform(T)
        scenes.append(c)

scene = trimesh.Scene(scenes)
scene.show()