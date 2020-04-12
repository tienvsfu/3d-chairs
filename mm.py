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
## fix width 
if arm_exist==True:
    armw = arm.vertices[:,0].max()-arm.vertices[:,0].min()
seatw = seat.vertices[:,0].max()-seat.vertices[:,0].min()
backw = back.vertices[:,0].max()-back.vertices[:,0].min()
legw = leg.vertices[:,0].max()-leg.vertices[:,0].min()

print(seatw)
if arm_exist==True:
    arm.verticies = arm.vertices * (seatw/armw)
back.verticies = back.vertices * (seatw/backw)
leg.verticies = leg.vertices * (seatw/legw)

# ## fix height
# back.verticies -= back.vertices[:,1].min()-seat.vertices[:,1].max()
# leg.verticies -= leg.vertices[:,1].max()-seat.vertices[:,1].min()

# random deformation
# translation, rotation


# render
if arm_exist==True:
    chair = trimesh.Scene([arm,back,leg,seat])
else:
    chair = trimesh.Scene([back,leg,seat])

chair.export('chair.obj')
chair.show()