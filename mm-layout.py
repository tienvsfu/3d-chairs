import trimesh
import random 
from mm import *

o = 0
n = 6
chairs = []

while o<n:
    try:
        mm(o,False)
    except:
        continue
    ob = trimesh.load(str(o)+'.obj')

    for i in range(len(ob.vertices)):
        cols = int(o%3)
        rows = int(o/3)
        ob.vertices[i][0] = ob.vertices[i][0]+(3*cols)
        ob.vertices[i][1] = ob.vertices[i][1]+(3*rows)
    chairs.append(ob)
    o += 1

scene = trimesh.Scene(chairs)
scene.show()