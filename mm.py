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

# fix relative size and position 

# size
if arm_exist==True:
    armw = arm.vertices[:,0].max()-arm.vertices[:,0].min()
seatw = seat.vertices[:,0].max()-seat.vertices[:,0].min()
backw = back.vertices[:,0].max()-back.vertices[:,0].min()
legw = leg.vertices[:,0].max()-leg.vertices[:,0].min()

if arm_exist==True:
    scale = seatw/armw
    for i in range(len(arm.vertices)):
        arm.vertices[i] = arm.vertices[i]*scale 
scale = seatw/backw
for i in range(len(back.vertices)):
    back.vertices[i] = back.vertices[i]*scale 
scale = seatw/legw
for i in range(len(leg.vertices)):
    leg.vertices[i] = leg.vertices[i]*scale

# # position
# if arm_exist==True:
#     armh = seat.vertices[:,1].min()-arm.vertices[:,1].max()
# backh = seat.vertices[:,1].max()-back.vertices[:,1].min()
# legh = seat.vertices[:,1].min()-leg.vertices[:,1].max()


# ## fix height
# back.verticies -= 
# leg.verticies -= 

# deformation --> widen and rotate

# fix connections

# render
if arm_exist==True:
    chair = trimesh.Scene([arm,back,leg,seat])
else:
    chair = trimesh.Scene([back,leg,seat])

chair.export('chair.obj')
chair.show()