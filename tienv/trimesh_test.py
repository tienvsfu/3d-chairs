import numpy as np
import trimesh
import pdb
import os
import random

from icp import icp
from trimesh.transformations import scale_matrix, translation_matrix
from utils import is_cubic

random.seed(2)
shift_X = 1

# attach to logger so trimesh messages will be printed to console
# trimesh.util.attach_to_log()

# by default, Trimesh will do a light processing, which will
# remove any NaN values and merge vertices that share position
# if you want to not do this on load, you can pass `process=False`
mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0]],
                       faces=[[0, 1, 2]],
                       process=False)

all_chairs_dir = '../data/chairs/'
# seat_meshes = []
# back_meshes = []
chair_meshes = []

chair_dirs = os.listdir(all_chairs_dir)

for chair_dir in chair_dirs:
    seat_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'seat.obj')
    back_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'back.obj')

    seat_mesh = trimesh.load(seat_mesh_dir)
    back_mesh = trimesh.load(back_mesh_dir)
    chair_meshes.append((seat_mesh, back_mesh))

# scenes = seat_meshes
random_chairs = random.sample(chair_meshes, 2)

# move the original chair for illustration
original_chair = random_chairs[0]
second_chair_render = [r.copy() for r in random_chairs[1]]
T = translation_matrix([shift_X, 0, 0])
[p.apply_transform(T) for p in second_chair_render]

# display original intersection
original_chair_intersect = original_chair[0].intersection(original_chair[1])
original_chair_intersect.apply_transform(T)

if len(original_chair_intersect.vertices) == 0:
    print("co intersect deo dau")

# display the intersection
first_seat = random_chairs[0][0].copy()
second_back = random_chairs[1][1].copy()
first_back_bb = random_chairs[0][1].bounding_box
second_back_bb = random_chairs[1][1].bounding_box

fb_bb_mesh = trimesh.Trimesh(vertices = first_back_bb.vertices, faces = first_back_bb.faces)
sb_bb_mesh = trimesh.Trimesh(vertices = second_back_bb.vertices, faces = second_back_bb.faces)
sz1 = np.abs(first_back_bb.vertices[0][1] - first_back_bb.vertices[2][1])
sz2 = np.abs(second_back_bb.vertices[0][1] - second_back_bb.vertices[2][1])

Sz = np.identity(4)
Sz[1][1] = sz2 / sz1
pdb.set_trace()

T0 = translation_matrix([shift_X * 2, 0, 0])
fb_bb_mesh.apply_transform(Sz)
furthest_y_orig = first_back_bb.vertices[:,1].max()
furthest_y_now = fb_bb_mesh.vertices[:,1].max()
TF = translation_matrix([0, furthest_y_orig - furthest_y_now, 0])
fb_bb_mesh.apply_transform(TF)

fb_bb_mesh.apply_transform(T0)
sb_bb_mesh.apply_transform(T0)
# pdb.set_trace()

# fv = first_back_bb.vertices
# sv = second_back_bb.vertices

fv = first_back_bb.sample_volume(count=100)
sv = second_back_bb.sample_volume(count=100)

# TT, _, _ = icp(fv, sv)
# first_seat.apply_transform(TT)

# shift the modified seat
T1 = translation_matrix([shift_X * 3, 0, 0])
first_seat.apply_transform(T1)
second_back.apply_transform(T1)

intersection = first_seat.intersection(second_back)
T2 = translation_matrix([shift_X, 0, 0])
intersection.apply_transform(T2)

# pdb.set_trace()

scenes = [
    original_chair[0],
    original_chair[1],
    second_chair_render[0],
    second_chair_render[1],
    fb_bb_mesh,
    sb_bb_mesh,
    first_seat,
    second_back,
    intersection
]

# pdb.set_trace()
scene = trimesh.Scene(scenes)

scene.show()