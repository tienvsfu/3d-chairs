def combine_meshes(meshes):
    arm_exist = False

    if len(meshes) == 4:
        arm_exist = True
        seat, back, leg, arm = meshes
    else:
        seat, back, leg = meshes

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

    rtn_meshes = [seat, back, leg]
    
    if arm_exist:
        rtn_meshes.append(arm)

    return rtn_meshes