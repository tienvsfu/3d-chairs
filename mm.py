import trimesh
import random 

# mix
n = 10
c = [173,347,470,515,688,1095,1325,2820,3001,39101]
a = random.randint(0,n-1)
b = random.randint(0,n-1)
l = random.randint(0,n-1)
s = random.randint(0,n-1)

arm_exist = True
try: 
    arm = trimesh.load('chairs/'+str(c[a])+'/arm.obj')
    arm.visual.face_colors = [200,100,100,100]
except:
    arm_exist = False

back = trimesh.load('chairs/'+str(c[b])+'/back.obj')
leg = trimesh.load('chairs/'+str(c[l])+'/leg.obj')
seat = trimesh.load('chairs/'+str(c[s])+'/seat.obj')

back.visual.face_colors = [100,200,100,100]
leg.visual.face_colors = [100,100,200,100]
seat.visual.face_colors = [100,100,100,200]

# match
# scale, translation, rotation

# render
if arm_exist==True:
    chair = trimesh.Scene([arm,back,leg,seat])
else:
    chair = trimesh.Scene([back,leg,seat])

chair.export('chair.obj')
chair.show()