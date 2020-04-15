import trimesh
import random 
from mm import *

def generate(n,c):
    o = 0
    while o<n:
        try:
            mm(o,False,c)
        except:
            continue
        o += 1