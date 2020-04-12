import numpy as np
import trimesh
import pdb
import os
import random

from trimesh.transformations import scale_matrix, translation_matrix
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
from utils import layout

random.seed(2)
shift_X = 3

all_chairs_dir = './chairs/'
chair_meshes = []

chair_dirs = os.listdir(all_chairs_dir)

for chair_dir in chair_dirs:
    seat_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'seat.obj')
    back_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'back.obj')
    leg_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'leg.obj')
    arm_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'arm.obj')

    seat_mesh = trimesh.load(seat_mesh_dir)
    back_mesh = trimesh.load(back_mesh_dir)
    leg_mesh = trimesh.load(leg_mesh_dir)

    chair_mesh = [seat_mesh, back_mesh, leg_mesh]

    if os.path.isdir(arm_mesh_dir):
        arm_mesh = trimesh.load(arm_mesh_dir)
        chair_mesh.append(arm_mesh)

    chair_meshes.append(chair_mesh)

scenes = layout(chair_meshes)
scene = trimesh.Scene(scenes)

scene.show()