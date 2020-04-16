import numpy as np
import trimesh
import pdb
import os
import random

from trimesh.transformations import scale_matrix, translation_matrix
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
from utils import preprocess, layout
from deformations import *
from mesh_combine import combine_meshes
from colour import Color

random.seed(2)

N_chairs_to_generate = 9
P_has_arm = 0.1
all_chairs_dir = './chairs/'
chair_dirs = os.listdir(all_chairs_dir)

n = int(len(chair_dirs) / 3)
r_to_g = list(Color("red").range_to(Color("green"), n))
g_to_b = list(Color("green").range_to(Color("blue"), n))
b_to_r = list(Color("blue").range_to(Color("red"), len(chair_dirs) - 2 * n))
color_gradient = r_to_g + g_to_b + b_to_r

seat_meshes = []
back_meshes = []
leg_meshes = []
arm_meshes = []

def processed_load(mesh_dir):
    return preprocess(trimesh.load(mesh_dir))

# read the stuff in
for i, chair_dir in enumerate(chair_dirs):
    seat_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'seat.obj')
    back_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'back.obj')
    leg_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'leg.obj')
    arm_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'arm.obj')

    seat_mesh = processed_load(seat_mesh_dir)
    back_mesh = processed_load(back_mesh_dir)
    leg_mesh = processed_load(leg_mesh_dir)
 
    # color
    (r, g, b) = color_gradient[i].get_rgb()
    r *= 255
    g *= 255
    b *= 255

    # pdb.set_trace()
    if seat_mesh is not None:
        seat_mesh.visual.face_colors = [r,g,b,100]
        seat_meshes.append(seat_mesh)

    if back_mesh is not None:
        back_mesh.visual.face_colors = [r,g,b,100]
        back_meshes.append(back_mesh)

    if leg_mesh is not None:
        leg_mesh.visual.face_colors = [r,g,b,100]
        leg_meshes.append(leg_mesh)

    if os.path.isfile(arm_mesh_dir):
        arm_mesh = processed_load(arm_mesh_dir)

        if arm_mesh is not None:
            arm_mesh.visual.face_colors = [r,g,b,100]
            arm_meshes.append(arm_mesh)

# add custom deformed parts
seat_meshes += generate_seat_deformations(seat_meshes)
back_meshes += generate_back_deformations(back_meshes)
leg_meshes += generate_back_deformations(leg_meshes)
arm_meshes += generate_back_deformations(arm_meshes)

generated_chair_meshes = []
for i in range(N_chairs_to_generate):
    random_seat = random.choice(seat_meshes)
    random_back = random.choice(back_meshes)
    random_leg = random.choice(leg_meshes)

    chair_mesh = [random_seat.copy(), random_back.copy(), random_leg.copy()]

    if random.random() < P_has_arm:
        chair_mesh.append(random.choice(arm_meshes).copy())

    chair_mesh = combine_meshes(chair_mesh)
    generated_chair_meshes.append(chair_mesh)

scenes = layout(generated_chair_meshes)
scene = trimesh.Scene(scenes)

scene.show()