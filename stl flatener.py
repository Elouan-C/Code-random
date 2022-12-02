import time

def normal(p1,p2,p3): #vectorial product
    v1=[ p2[0]-p1[0] , p2[1]-p1[1] , p2[2]-p1[2] ]
    v2=[ p3[0]-p1[0] , p3[1]-p1[1] , p3[2]-p1[2] ]

    a = v1[1]*v2[2]-v1[2]*v2[1]
    b = v1[2]*v2[0]-v1[0]*v2[2]
    c = v1[0]*v2[1]-v1[1]*v2[0]

    return [a,b,c]

def facet(p1,p2,p3):
    nv = normal(p1,p2,p3) #normal vector
    facet_list = []
    facet_list.append(''.join(["  facet normal ",str(nv[0])," ",str(nv[1])," ",str(nv[2]),"\n"]))
    facet_list.append(         "    outer loop\n")
    facet_list.append(''.join(["      vertex ",str(p1[0]),' ',str(p1[1]),' ',str(p1[2]),'\n']))
    facet_list.append(''.join(["      vertex ",str(p2[0]),' ',str(p2[1]),' ',str(p2[2]),'\n']))
    facet_list.append(''.join(["      vertex ",str(p3[0]),' ',str(p3[1]),' ',str(p3[2]),'\n']))
    facet_list.append(         "    endloop\n")
    facet_list.append(         "  endfacet\n")
    facet_str = ''.join(facet_list)
    return facet_str

def stl_writer(triangles,points,file_name):
    #triangles[0] = [1,3,4]
    #the first triangle is formed by the points 1; 3 and 4

    #points[0] = [10,5,20]
    #the list "points" contains lists with [x,y,z] data

    f= open(file_name,"w")

    stl_list = ["solid ASCII\n"]

    for tri in triangles:
        p1 = points[tri[0]]
        p2 = points[tri[1]]
        p3 = points[tri[2]]

        stl_list.append(facet(p1,p2,p3))

    stl_list.append("endsolid")

    stl_str = ''.join(stl_list)

    f.write(stl_str)
    f.close()


def stl_reader(file_name):
    text_file = open(file_name, "r")
    raw_tri = text_file.read().split('endloop')[:-1]
    text_file.close()

    #extracting the (x,y,z) coordinates of the triangles in the stl file
    for i in range(len(raw_tri)):
        raw_tri[i] = raw_tri[i].split('vertex')[-3:]
        for j in range(3):
            raw_tri[i][j] = raw_tri[i][j].split('\n')[0]
            raw_tri[i][j] = raw_tri[i][j].split(' ')
            raw_tri[i][j] = list(filter(lambda a: a != '', raw_tri[i][j])) #https://stackoverflow.com/questions/1157106/remove-all-occurrences-of-a-value-from-a-list
            for k in range(3):
                raw_tri[i][j][k] = float(raw_tri[i][j][k])

    #removing dentical points and reformating the triangle data
    point_list = raw_tri[0]
    triangles = [[0,1,2]]
    
    for tri in raw_tri[1:]:
        triangles.append([])
        
        for pnt in tri:
            if pnt not in point_list:
                point_list.append(pnt)
            triangles[-1].append(point_list.index(pnt))
                
                
    
    return point_list,triangles

def rectifier(points,target,tolerance): #snap all the points in the tolerance range to the z target value in order to have a flat surface
    counter = 0
    if type(target) is not list:
        target = [target]
    for i in range(len(target)):
        tar = float(target[i])
        if type(tolerance) is list:
            tol = float(tolerance[i])
        else:
            tol = float(tolerance)
        mini = tar-tol
        maxi = tar+tol
        
        for j in range(len(points)):
            z = points[j][2]

            if (mini <= z) and (z <= maxi):
                points[j][2] = tar
                counter +=1
    print(counter,"points adjusted")
    return points

def flatten(file_name,ztarget,tolerance):
    file_name2 = ''.join([file_name[:-4], '_2.stl'])

    t0 = time.time()
    pnt,tri = stl_reader(name)
    t1 = time.time()
    print("read stl in",t1-t0,"sec")
    
    pnt = rectifier(pnt,ztarget,tolerance)
    t2 = time.time()
    print("rectified stl in",t2-t1,"sec")
    
    stl_writer(tri,pnt,file_name2)
    t3 = time.time()
    print("wrote stl in",t3-t2,"sec")
    print("exported to:",file_name2)
          
"""
TEST
"""

point_pyramide=[[0,0,-0.1],
                [0,1,0.2],
                [1,0,0.1],
                [0.5,0.5,1]]
tri_pyramide=[[0,1,2],
              [0,1,3],
              [0,2,3],
              [1,2,3]]

name = "test.stl"

stl_writer(tri_pyramide,point_pyramide,name)

name = "maillage_structure_interne_2_evider_reduced.stl"
flatten(name,[4,6,-6,-4],1.5)#[0.5,0.5,1]
