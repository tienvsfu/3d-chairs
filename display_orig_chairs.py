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

all_chairs_dir = './data/mm'
chair_meshes = []

chair_dirs = os.listdir(all_chairs_dir)

for chair_dir in chair_dirs:
    chair_mesh = trimesh.load(os.path.join(all_chairs_dir, chair_dir))
    chair_meshes.append([chair_mesh])

scenes = layout(chair_meshes)
scene = trimesh.Scene(scenes)

scene.show()