import numpy as np
from math import pi as pi
from trimesh.transformations import rotation_matrix, translation_matrix
import pdb
shift_X = 3

def layout(meshes):
    scenes = []
    ncols = nrows = int(np.ceil(np.sqrt(len(meshes))))

    for i in range(nrows):
        T_x = shift_X * i

        for j in range(ncols):
            index = i * nrows + j

            if index >= len(meshes):
                break

            T_y = shift_X * j
            T = translation_matrix([T_x, T_y, 0])
            
            c = meshes[index]
            [part.apply_transform(T) for part in c]
            scenes.extend(c)

    return scenes

# should be automatic, globally align the mesh so its easier to work with
def preprocess(mesh):
    R = rotation_matrix(0, [1, 0, 0])
    mesh = mesh.apply_transform(R)

    return mesh