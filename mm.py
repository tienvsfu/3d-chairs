import trimesh
import random 

def mm(obs,display,c):
    print("obs: "+str(obs))
    # mix
    
    # c = [173,347,470,515,688,1095,1325,2820,3001,39101]
    n = len(c)
    ida = random.randint(0,n-1)
    idb = random.randint(0,n-1)
    idl = random.randint(0,n-1)
    ids = random.randint(0,n-1)

    arm_exist = True
    try: 
        arm = trimesh.load('data/out/'+str(c[ida])+'/arm.obj')
    except:
        arm_exist = False

    back = trimesh.load('data/out/'+str(c[idb])+'/back.obj')
    leg = trimesh.load('data/out/'+str(c[idl])+'/leg.obj')
    seat = trimesh.load('data/out/'+str(c[ids])+'/seat.obj')

    ## deform 
    if arm_exist==True:
        s = random.uniform(0.75,1.15)
        for i in range(len(arm.vertices)):
            arm.vertices[i][2] = arm.vertices[i][2]*s  
    s = random.uniform(0.75,1.15)
    for i in range(len(back.vertices)):
        back.vertices[i][2] = back.vertices[i][2]*s  
    s = random.uniform(0.75,1.15)
    for i in range(len(leg.vertices)):
        leg.vertices[i][2] = leg.vertices[i][2]*s 
    s = random.uniform(0.75,1.15)
    for i in range(len(seat.vertices)):
        seat.vertices[i][2] = seat.vertices[i][2]*s 

    ## rotate
    r = random.uniform(-0.2,0)
    rm = trimesh.transformations.rotation_matrix(r,[1,0,0],back.centroid)
    back.apply_transform(rm)

    # match 

    ## fix size (x)
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

    ## fix size (z)
    if arm_exist==True:
        armd = arm.vertices[:,2].max()-arm.vertices[:,2].min()
    seatd = seat.vertices[:,2].max()-seat.vertices[:,2].min()
    legd = leg.vertices[:,2].max()-leg.vertices[:,2].min()
    backd = back.vertices[:,2].max()-back.vertices[:,2].min()
    if arm_exist==True:
        scale = seatd/armd 
        for i in range(len(arm.vertices)):
            arm.vertices[i][2] = arm.vertices[i][2]*scale 
    scale = seatd/legd 
    for i in range(len(leg.vertices)):
        leg.vertices[i][2] = leg.vertices[i][2]*scale 
    scale = seatd/backd
    s = random.uniform(0.2,0.4)
    for i in range(len(back.vertices)):
        back.vertices[i][2] = back.vertices[i][2]*(s*scale)

    ## fix position (y)
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
        
    ## fix position (z)
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

    ## fix connections
    if arm_exist==True:
        arm = trimesh.intersections.slice_mesh_plane(arm, plane_normal=[0,1,0], plane_origin=seat.centroid)
    back = trimesh.intersections.slice_mesh_plane(back, plane_normal=[0,1,0], plane_origin=seat.centroid)
    leg = trimesh.intersections.slice_mesh_plane(leg, plane_normal=[0,-1,0], plane_origin=seat.centroid)

    # color
    # print('color')
    if arm_exist==True:
        t1 = int(c[ida])%256
        t2 = int(c[ida]/3)%256
        t3 = int(c[ida]/7)%256
        arm.visual.face_colors = [t1,t2,t3,100]
    t1 = int(c[idb])%256
    t2 = int(c[idb]/3)%256
    t3 = int(c[idb]/7)%256
    back.visual.face_colors = [0+t1,0+t2,0+t3,100]
    t1 = int(c[idl])%256
    t2 = int(c[idl]/3)%256
    t3 = int(c[idl]/7)%256
    leg.visual.face_colors = [0+t1,0+t2,0+t3,100]
    t1 = int(c[ids])%256
    t2 = int(c[ids]/3)%256
    t3 = int(c[ids]/7)%256
    seat.visual.face_colors = [0+t1,0+t2,0+t3,100]

    # export
    if arm_exist==True:
        chair = trimesh.Scene([arm,back,leg,seat])
    else:
        chair = trimesh.Scene([back,leg,seat])

    chair.export('data/mm/'+str(obs)+'.obj')

    if display==True:
        chair.show()

# if u want to generate one
# c10 = [2585, 2323, 43872]
# mm(100,True,c10)

def generate(n,c):
    o = 0
    while o<n:
        try:
            mm(o,False,c)
        except:
            continue
        o += 1
        

def display(ranking):
    chairs = []
    for o in range(len(ranking)):
        ob = trimesh.load('data/mm/'+str(ranking[o])+'.obj')
        for i in range(len(ob.vertices)):
            cols = int(o%3)
            rows = int(o/3)
            ob.vertices[i][0] = ob.vertices[i][0]+(3*cols)
            ob.vertices[i][1] = ob.vertices[i][1]+(3*rows)
        chairs.append(ob)
    scene = trimesh.Scene(chairs)
    scene.show()

