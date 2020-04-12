import numpy as np
from math import pi as pi

# depth of deformation
MULP = 0.4

# higher = more of flat back
DELTA = 0.5

# modify Z
curve_index = 2
curve_fn = np.cos

def curve2(mesh):
    max_x = mesh.vertices[:, 0].max()
    min_x = mesh.vertices[:, 0].min()

    mid_x = (max_x + min_x) / 2
    d = np.abs(mid_x - min_x)

    for i in range(len(mesh.vertices)):
        # 1 to 0, 0 to 1
        t = np.abs(mesh.vertices[i][0] - mid_x) / d
        mesh.vertices[i][curve_index] -= curve_fn(t * pi/2) * MULP

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
    Y_line = curve_fn(0 * pi/2) * MULP

    for i in range(len(mesh.vertices)):
        x = mesh.vertices[i][0]

        if x < left_X:
            # 1 to 0
            t = np.abs(x - left_X) / d
            mesh.vertices[i][curve_index] -= curve_fn(t * pi/2) * MULP
        elif x < right_X:
            # 1 to 0, 0 to 1
            t = np.abs(x - mid_x) / d_mid
            mesh.vertices[i][curve_index] -= Y_line
        else:
            t = np.abs(x - right_X) / d
            mesh.vertices[i][curve_index] -= curve_fn(t * pi/2) * MULP

    return mesh

def generate_back_deformations(meshes):
    curve2s = [curve2(mesh.copy()) for mesh in meshes]
    curve3s = [curve3(mesh.copy()) for mesh in meshes]

    return curve2s + curve3s

def generate_seat_deformations(meshes):
    return []

def generate_arm_deformations(meshes):
    return []

def generate_legs_deformations(meshes):
    return []