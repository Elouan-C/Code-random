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
    

"""
TEST
"""

point_pyramide=[[0,0,0],
                [0,1,0],
                [1,0,0],
                [0.5,0.5,1]]
tri_pyramide=[[0,1,2],
              [0,1,3],
              [0,2,3],
              [1,2,3]]

name = "test.stl"
stl_writer(tri_pyramide,point_pyramide,name)

pnt,tri = stl_reader(name)
print("pnt:\n",pnt)
print("tri:\n",tri)
stl_writer(tri,pnt,'test2.stl')
