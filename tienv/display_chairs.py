import numpy as np
import trimesh
import pdb
import os
import random

from trimesh.transformations import scale_matrix, translation_matrix
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon

random.seed(2)
shift_X = 3

# attach to logger so trimesh messages will be printed to console
# trimesh.util.attach_to_log()

# by default, Trimesh will do a light processing, which will
# remove any NaN values and merge vertices that share position
# if you want to not do this on load, you can pass `process=False`
mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0]],
                       faces=[[0, 1, 2]],
                       process=False)

all_chairs_dir = '../chairs/'
# seat_meshes = []
# back_meshes = []
chair_meshes = []

chair_dirs = os.listdir(all_chairs_dir)
EPSILON = 0.055

def hullify_2D(vertices):
    as_np = np.array(vertices)
    # as_np[as_np[:,0].argsort()]
    as_np = np.delete(as_np, 2, 1)
    hull = ConvexHull(as_np)
    
    hull_np = np.zeros((hull.vertices.shape[0], 3))
    hull_np[:, :2] = [as_np[i] for i in hull.vertices]

    return hull_np

def area_2D(points):
    as_np = np.delete(points, 2, 1)
    polygon = Polygon(as_np)

    return polygon.area

def meshify_2d(vertices):
    pc = trimesh.points.PointCloud(vertices)
    centroid = pc.centroid

    new_vertices = vertices.copy()
    new_vertices = np.concatenate((new_vertices, [centroid]))
    centroid_index = len(new_vertices) - 1
    faces = []

    for i in range(len(vertices)):
        face = (centroid_index, i, i+1)
        faces.append(face)

    new_mesh = trimesh.Trimesh(vertices=new_vertices, faces=faces)
    return new_mesh

def preprocess_seat(mesh):
    for i in range(len(mesh.vertices)):
        mesh.vertices[i][2] = 0

for chair_dir in chair_dirs:
    seat_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'seat.obj')
    back_mesh_dir = os.path.join(all_chairs_dir, chair_dir, 'back.obj')

    seat_mesh = trimesh.load(seat_mesh_dir)
    back_mesh = trimesh.load(back_mesh_dir)
    chair_meshes.append((seat_mesh, back_mesh))

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
        [part.apply_transform(T) for part in c]
        scenes.extend(c)

# pdb.set_trace()
scene = trimesh.Scene(scenes)

scene.show()