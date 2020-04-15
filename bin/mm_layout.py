import trimesh
import random 
from mm import *


def display(n):
    o = 0
    chairs = []

    while o<n:
        ob = trimesh.load('data/mm/'+str(o)+'.obj')
        for i in range(len(ob.vertices)):
            cols = int(o%3)
            rows = int(o/3)
            ob.vertices[i][0] = ob.vertices[i][0]+(3*cols)
            ob.vertices[i][1] = ob.vertices[i][1]+(3*rows)
        chairs.append(ob)
        o += 1

    scene = trimesh.Scene(chairs)
    scene.show()

