import trimesh
import random 
from mm import *

n = 5
chairs = []

for obs in range(n):
    mm(obs)
    ob = trimesh.load(str(obs)+'.obj')
    for i in range(len(ob.vertices)):
        ob.vertices[i][0] = ob.vertices[i][0]+(2*obs)
    chairs.append(ob)

scene = trimesh.Scene(chairs)
scene.show()