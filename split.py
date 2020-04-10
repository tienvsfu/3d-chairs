import os 

def split(d):
    c1 = 0
    c2 = 0
    o = ".obj"
    p = d+o
    # print(p)
    f1 = open(p)
    try:
        os.mkdir(d)
    except:
        pass

    for l in f1:
        if l[0]=='g': 
            p = d+'/'+l[2:-1]+o
            # print(p)
            f2 = open(p,"w+")
            c2 = c1
        if l[0]=='f':
            i1 = l.find(" ")+1
            i2 = l.find(" ",i1+1) +1
            i3 = l.find(" ",i2+1) +1
            print(int(l[i1:i2]))
            print(int(l[i2:i3]))
            print(int(l[i3:-1]))
            print(c2)
        f2.write(l)
        c1 += 1

d = "173"
split(d)