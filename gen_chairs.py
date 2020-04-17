import trimesh
import random
import os
import pdb
import numpy as np

def color_part(mesh, chair_id):
    if not mesh.is_empty:
        t1 = int(chair_id)%100
        t2 = int(chair_id/5)%100
        t3 = int(chair_id/8)%100
        mesh.visual.face_colors = [100+t3,100+t2,100+t1,100]
    
def gen_chairs(path_to_chairs, path_to_output, n_times=10, display=False):
    chair_dirs = os.listdir(path_to_chairs)

    if not os.path.isdir(path_to_output):
        os.mkdir(path_to_output)

    print(f'Generating {n_times} chairs')

    generated_chairs = []
    iter = 0

    while iter < n_times:
        n = len(chair_dirs)
        ida = random.randint(0,n-1)
        idb = random.randint(0,n-1)
        idl = random.randint(0,n-1)
        ids = random.randint(0,n-1)

        arm_id = chair_dirs[ida]
        back_id = chair_dirs[idb]
        leg_id = chair_dirs[idl]
        seat_id = chair_dirs[ids]

        # pdb.set_trace()

        arm_exist = True
        try: 
            arm = trimesh.load(os.path.join(path_to_chairs, arm_id, 'arm.obj'))
        except:
            arm_exist = False

        back = trimesh.load(os.path.join(path_to_chairs, back_id, 'back.obj'))
        leg = trimesh.load(os.path.join(path_to_chairs, leg_id, 'leg.obj'))
        seat = trimesh.load(os.path.join(path_to_chairs, seat_id, 'seat.obj'))

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

        # these better be int IDs
        arm_id = int(arm_id)
        back_id = int(back_id)
        leg_id = int(leg_id)
        seat_id = int(seat_id)

        # color
        # print('color')
        if arm_exist==True:
            t1 = int(arm_id)%100
            t2 = int(arm_id/5)%100
            t3 = int(arm_id/8)%100
            arm.visual.face_colors = [100+t3,100+t2,100+t1,100]

        # if not back.is_empty:
        t1 = int(back_id)%100
        t2 = int(back_id/5)%100
        t3 = int(back_id/8)%100
        back.visual.face_colors = [100+t3,100+t2,100+t1,100]

        # if not leg.is_empty:
        t1 = int(leg_id)%100
        t2 = int(leg_id/5)%100
        t3 = int(leg_id/8)%100
        leg.visual.face_colors = [100+t3,100+t2,100+t1,100]

        # if not seat.is_empty:
        t1 = int(seat_id)%100
        t2 = int(seat_id/5)%100
        t3 = int(seat_id/8)%100
        seat.visual.face_colors = [100+t3,100+t2,100+t1,100]

        # export
        if arm_exist==True:
            chair = trimesh.Scene([arm,back,leg,seat])
            # chair = arm + back + leg + seat
        else:
            # chair = back + leg + seat
            chair = trimesh.Scene([back,leg,seat])

        try:
            # unfortunately exporting the mesh directly doesn't work
            chair_path = os.path.join(path_to_output, f'{str(iter)}.obj')
            chair.export(chair_path)
            chair_as_mesh = trimesh.load(chair_path)

            generated_chairs.append(chair_as_mesh)
            print(f'Generated chair {iter}')
            iter += 1
        except Exception as e:
            # pdb.set_trace()
            # iter -= 1
            continue

        if display==True:
            chair.show()

    return generated_chairs

def display(ordered_meshes):
    chairs = []
    grid_len = np.ceil(np.sqrt(len(ordered_meshes)))

    for o, ob in enumerate(ordered_meshes):
        for i in range(len(ob.vertices)):
            cols = int(o%grid_len)
            rows = int(o/grid_len)
            ob.vertices[i][0] += 3 * cols
            ob.vertices[i][1] -= 3 * rows
        chairs.append(ob)
    scene = trimesh.Scene(chairs)
    scene.show()

