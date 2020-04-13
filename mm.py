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
except:
    arm_exist = False

back = trimesh.load('chairs/'+str(c[b])+'/back.obj')
leg = trimesh.load('chairs/'+str(c[l])+'/leg.obj')
seat = trimesh.load('chairs/'+str(c[s])+'/seat.obj')

# if arm_exist==True:
    # arm = trimesh.convex.convex_hull(arm)
# back = trimesh.convex.convex_hull(back)
# leg = trimesh.convex.convex_hull(leg)
# seat = trimesh.convex.convex_hull(seat)

# match

# deform 
if arm_exist==True:
    s = random.uniform(0.85,1.15)
    for i in range(len(arm.vertices)):
        arm.vertices[i][2] = arm.vertices[i][2]*s  
s = random.uniform(0.85,1.15)
for i in range(len(back.vertices)):
    back.vertices[i][2] = back.vertices[i][2]*s  
s = random.uniform(0.85,1.15)
for i in range(len(leg.vertices)):
    leg.vertices[i][2] = leg.vertices[i][2]*s 
s = random.uniform(0.85,1.15)
for i in range(len(seat.vertices)):
    seat.vertices[i][2] = seat.vertices[i][2]*s 

# rotate
r = random.uniform(-0.1,0)
rm = trimesh.transformations.rotation_matrix(r,[1,0,0],back.centroid)
back.apply_transform(rm)

# fix size (x)
if arm_exist==True:
    armw = arm.vertices[:,0].max()-arm.vertices[:,0].min()
seatw = seat.vertices[:,0].max()-seat.vertices[:,0].min()
backw = back.vertices[:,0].max()-back.vertices[:,0].min()
legw = leg.vertices[:,0].max()-leg.vertices[:,0].min()
if arm_exist==True:
    scale = seatw/armw
    for i in range(len(arm.vertices)):
        arm.vertices[i][0] = arm.vertices[i][0]*scale 
scale = seatw/backw
for i in range(len(back.vertices)):
    back.vertices[i][0] = back.vertices[i][0]*scale 
scale = seatw/legw
for i in range(len(leg.vertices)):
    leg.vertices[i][0] = leg.vertices[i][0]*scale

# fix size (z)
if arm_exist==True:
    armd = arm.vertices[:,2].max()-arm.vertices[:,2].min()
seatd = seat.vertices[:,2].max()-seat.vertices[:,2].min()
legd = leg.vertices[:,2].max()-leg.vertices[:,2].min()
if arm_exist==True:
    scale = seatd/armd 
    for i in range(len(arm.vertices)):
        arm.vertices[i][2] = arm.vertices[i][2]*scale 
scale = seatd/legd 
for i in range(len(leg.vertices)):
    leg.vertices[i][2] = leg.vertices[i][2]*scale 

# fix position (y)
if arm_exist==True:
    army = seat.vertices[:,1].min()-arm.vertices[:,1].min()
backy = seat.vertices[:,1].min()-back.vertices[:,1].min()
legy = seat.vertices[:,1].max()-leg.vertices[:,1].max()

if arm_exist==True:
    for i in range(len(arm.vertices)):
        arm.vertices[i][1] = arm.vertices[i][1]+army  
for i in range(len(back.vertices)):
    back.vertices[i][1] = back.vertices[i][1]+backy  
for i in range(len(leg.vertices)):
    leg.vertices[i][1] = leg.vertices[i][1]+legy 

# fix position (z)
if arm_exist==True:
    armz = seat.vertices[:,2].min()-arm.vertices[:,2].min()
backz = seat.vertices[:,2].min()-back.vertices[:,2].min()
legz = seat.vertices[:,2].min()-leg.vertices[:,2].min()

if arm_exist==True:
    for i in range(len(arm.vertices)):
        arm.vertices[i][2] = arm.vertices[i][2]+armz  
for i in range(len(back.vertices)):
    back.vertices[i][2] = back.vertices[i][2]+backz  
for i in range(len(leg.vertices)):
    leg.vertices[i][2] = leg.vertices[i][2]+legz 

# fix connections
if arm_exist==True:
    arm = arm.difference(seat)
    arm = arm.difference(back)
    arm = arm.difference(leg)
leg = leg.difference(seat)
leg = leg.difference(back)
back = back.difference(seat)

# color
if arm_exist==True:
    arm.visual.face_colors = [200,100,100,100]
back.visual.face_colors = [100,200,100,100]
leg.visual.face_colors = [100,100,200,100]
seat.visual.face_colors = [100,100,100,200]

# render
if arm_exist==True:
    chair = trimesh.Scene([arm,back,leg,seat])
else:
    chair = trimesh.Scene([back,leg,seat])

chair.export('chair.obj')
chair.show()