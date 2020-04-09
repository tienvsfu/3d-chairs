from __future__ import print_function, division
from matplotlib import pyplot as plt

import numpy as np
import pdb
import random
from numpy import linalg as LA
from utils import *
from mpl_toolkits.mplot3d import Axes3D

def draw(ax, cornerpoints, color):
    def add_line(from_index, to_index):
        ax.plot([cornerpoints[from_index][0], cornerpoints[to_index][0]],
                [cornerpoints[from_index][1], cornerpoints[to_index][1]],
                [cornerpoints[from_index][2], cornerpoints[to_index][2]], c=color)

    for line in cube_lines:
        add_line(line[0], line[1])

def shuffle_parts(chairs):
    part_to_shuffle = 2
    first_part = chairs[0].get_part(part_to_shuffle)

    for i in range(len(chairs) - 1):
        other_chair_part = chairs[i + 1].get_part(part_to_shuffle)
        chairs[i].fit_part(part_to_shuffle, other_chair_part)

    chairs[len(chairs) - 1].fit_part(part_to_shuffle, first_part)
    return chairs 

def draw_same_part(chairs):
    fig = plt.figure(0)
    cmap = plt.get_cmap('jet_r')
    ax = Axes3D(fig)
    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_zlim(-LIM, LIM)

    numColors = len(chairs)

    for k, chair in enumerate(chairs):
        # crappy "grid", just shift by X and Y, assume 3x3
        shift_Y = (k - 1) * (0.9 * LIM)

        for i, cubes in enumerate(chair.parts):        
            color = cmap(float(i) / numColors)
            cubes = [translate(cube, Tx=0, Ty=shift_Y) for cube in cubes]

            for cube in cubes:
                draw(ax, cube, color)

    # try replacing the legs
    shift_X = 1 * (0.9 * LIM)
    
    for chair in chairs:
        chair.save()

    chairs = shuffle_parts(chairs)

    for k, chair in enumerate(chairs):
        # crappy "grid", just shift by X and Y, assume 3x3
        shift_Y = (k - 1) * (0.9 * LIM)

        for i, chair_part in enumerate(chair.parts):        
            color = cmap(float(i) / numColors)
            chair_part = [translate(cube, Tx=shift_X, Ty=shift_Y) for cube in chair_part]

            for cube in chair_part:
                draw(ax, cube, color)

    plt.show()

def showGenshape(recover_boxes, box_labels):
    print("Labels are", box_labels)

    cmap = plt.get_cmap('jet_r')
    fig = plt.figure(0)
    ax = Axes3D(fig)
    ax.set_xlim(-LIM, LIM)
    ax.set_ylim(-LIM, LIM)
    ax.set_zlim(-LIM, LIM)

    numColors = len(list(set(box_labels)))

    for jj in range(len(recover_boxes)): 
        label = float(box_labels[jj])
        points = recover_boxes[jj]
        color = cmap(label / numColors)

        draw(ax, points, color)
    plt.show()