import numpy as np
import pdb
import random
from numpy import linalg as LA
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
from constants import *

def apply_transform(A, T):
    assert A.shape[1] == 3
    assert T.shape[0] == 4

    A2 = np.ones((len(A), 4))
    A2[:, :3] = A
    # result = np.matmul(T, A2.T).T[:, :3]
    result = np.dot(T, A2.T).T[:, :3]
    return np.round(result, decimals=3)

def rotation_matrix(axis, theta):
    axis = axis/np.sqrt(np.dot(axis, axis))
    a = np.cos(theta/2.)
    b, c, d = -axis*np.sin(theta/2.)

    return np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a+c*c-b*b-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a+d*d-b*b-c*c]])

def scale(vertices, factor=0.5):
    S = np.array([[factor, 0, 0],
                  [0, factor, 0],
                  [0, 0, factor]])

    return np.matmul(S, vertices.T).T

def translate(vertices, Tx=0, Ty=0, Tz=0):
    new_vertices = vertices + [Tx, Ty, Tz]
    return new_vertices

def sample_cubes(cubes, n_times=100):
    sample_points = np.zeros((n_times, 3))

    for i in range(n_times):
        random_cube = random.choice(cubes)
        random_surface = random.choice(cube_surfaces)
        sample_point = sample_once(random_surface, random_cube)
        
        sample_points[i] = sample_point

    return sample_points

def sample_once(random_surface, vertices):
    (a, b, c, _) = random_surface
    A = vertices[a]
    B = vertices[b]
    C = vertices[c]

    same_index = 0

    for j in range(3):
        if A[j] == B[j] and B[j] == C[j]:
            same_index = j
            # print("Same plane is ", j)
            break

    sample_point = np.zeros((1, 3))
    pairs = [(A, B), (B, C)]
    pair_index = 0

    for j in range(3):
        if j == same_index:
            sample_point[:, j] = A[same_index]
        else:
            interp = random.uniform(0, 1)
            S = pairs[pair_index][0][j]
            D = pairs[pair_index][1][j]

            interp_point = interp * S + (1 - interp) * D
            # pdb.set_trace()
            sample_point[:, j] = interp_point

            pair_index += 1

    return sample_point

def sample_cube(vertices, n_times=100):
    sample_points = np.zeros((n_times, 3))

    for i in range(n_times):
        random_surface = random.choice(cube_surfaces)
        sample_point = sample_once(random_surface, vertices)
        
        sample_points[i] = sample_point

    return sample_points

def sensiblize(point_cloud):
    cubes = []

    for pc in point_cloud:
        pc_numpy = pc.squeeze(0).numpy()

        center = pc_numpy[0: 3]
        lengths = pc_numpy[3: 6]
        dir_1 = pc_numpy[6: 9]
        dir_2 = pc_numpy[9: ]

        dir_1 = dir_1/LA.norm(dir_1)
        dir_2 = dir_2/LA.norm(dir_2)
        dir_3 = np.cross(dir_1, dir_2)
        dir_3 = dir_3/LA.norm(dir_3)
        cube = np.zeros([8, 3])

        d1 = 0.5*lengths[0]*dir_1
        d2 = 0.5*lengths[1]*dir_2
        d3 = 0.5*lengths[2]*dir_3

        cube[0] = center - d1 - d2 - d3
        cube[1] = center - d1 + d2 - d3
        cube[2] = center + d1 - d2 - d3
        cube[3] = center + d1 + d2 - d3
        cube[4] = center - d1 - d2 + d3
        cube[5] = center - d1 + d2 + d3
        cube[6] = center + d1 - d2 + d3
        cube[7] = center + d1 + d2 + d3

        cubes.append(cube)

    return cubes

def draw_vertices(vertices, f=0):
    color = cmap(f)
    fig = plt.figure(0)
    ax = Axes3D(fig)
    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_zlim(-LIM, LIM)

    for vertex in vertices:
        ax.scatter([vertex[0]], [vertex[1]], [vertex[2]], c=np.array([color]))

    plt.show()


def is_cubic(seat_mesh):
    max_y = seat_mesh.vertices[:,1:2].max()
    min_y = seat_mesh.vertices[:,1:2].min()

    pc = np.array([f for f in seat_mesh.vertices if f[1] == min_y])
    pf = np.array([f for f in seat_mesh.vertices if f[1] == max_y])
    pc_min_x = pc[:,:1].min()
    pc_max_x = pc[:,:1].max()
    pf_min_x = pf[:,:1].min()
    pf_max_x = pf[:,:1].max()

    # points_furthest_min_x = points_furthest[:,:1].min()
    # points_furthest_max_x = points_furthest[:,:1].max()

    pdb.set_trace()
    bb = seat_mesh.bounding_box.vertices
    bb_min_x = bb[:,:1].min().item()
    bb_max_x = bb[:,:1].max().item()

    
    return True