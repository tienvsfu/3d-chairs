import trimesh
import random 
from mm import *

o = 0
n = 10
while o<n:
    try:
        mm(o,False)
    except:
        continue
    o += 1