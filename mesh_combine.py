def combine_meshes(meshes):
    arm_exist = False

    if len(meshes) == 4:
        arm_exist = True
        seat, back, leg, arm = meshes
    else:
        seat, back, leg = meshes

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
    if arm_exist==True:
        scale = seatd/armd 
        for i in range(len(arm.vertices)):
            arm.vertices[i][2] = arm.vertices[i][2]*scale 
    scale = seatd/legd 
    for i in range(len(leg.vertices)):
        leg.vertices[i][2] = leg.vertices[i][2]*scale 

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

    rtn_meshes = [seat, back, leg]
    
    if arm_exist:
        rtn_meshes.append(arm)

    return rtn_meshes