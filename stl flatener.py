import time
import tkinter as tk

pnt_list = []
tri_list = []
z_values = []

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

def open_file():
    t0 = time.time()
    global pnt_list
    global tri_list
    
    file_name_ = entry_file_name.get()
    print("opening file ...")
    pnt_list, tri_list =stl_reader(file_name_)
    t1 = time.time()
    print("file opened in",round(t1-t0,3),"sec")

def stl_reader(file_name):
    global pnt_list
    global tri_list
    global z_values
    
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

    #removing identical points and reformating the triangle data
    point_list = raw_tri[0]
    triangles = [[0,1,2]]
    
    for tri in raw_tri[1:]:
        triangles.append([])
        
        for pnt in tri:
            if pnt not in point_list:
                point_list.append(pnt)
                z_values.append(pnt[2])
            triangles[-1].append(point_list.index(pnt))
                
                
    
    return point_list,triangles

def rectifier(points,target,tolerance): #snap all the points in the tolerance range to the z target value in order to have a flat surface
    if len(tolerance) == 1:
        tolerance = tolerance[0]
    counter = 0
    if type(target) is not list:
        target = [target]
    for i in range(len(target)):
        tar = float(target[i])
        if type(tolerance) is list:
            if type(tolerance[i]) is not list:
                tol_inf = float(tolerance[i])
                tol_sup = tol_inf
            else:
                tol_inf = tolerance[i][0]
                tol_sup = tolerance[i][1]
        else:
            tol_inf = float(tolerance)
            tol_sup = tol_inf
        mini = tar - tol_inf
        maxi = tar + tol_sup
        
        for j in range(len(points)):
            z = points[j][2]

            if (mini <= z) and (z <= maxi):
                points[j][2] = tar
                counter +=1
    print(counter,"points adjusted")
    return points

def flatten(file_name,ztarget,tolerance):
    global pnt_list
    global tri_list
    file_name2 = ''.join([file_name[:-4], '_flatened.stl'])
    
    t0 = time.time()
    if pnt_list == [] and tri_list == []:
        pnt_list,tri_list = stl_reader(file_name)
        t1 = time.time()
        print("read stl in",t1-t0,"sec")
    t1 = time.time()
    
    pnt_list = rectifier(pnt_list,ztarget,tolerance)
    t2 = time.time()
    print("rectified stl in",t2-t1,"sec")
    
    stl_writer(tri_list,pnt_list,file_name2)
    t3 = time.time()
    print("wrote stl in",t3-t2,"sec")
    print("exported to:",file_name2)
    print("total run time:",t3-t0,'sec')
    return file_name2

def get_info(n):
    global z_values
    #print("z_values:",len(z_values))
    z_max = max(z_values)
    z_min = min(z_values)
    interval = (z_max-z_min)/n
    z_frequency_raw = []
    for i in range(n):
        z_frequency_raw.append([])
    z_frequency = []

    borne = []
    for i in range(n+1):
        borne.append( z_min +   i  *interval)

    #print("z_min   ",z_min)
    #print("z_max   ",z_max)
    #print("interval",interval)
    #print("borne   ",borne)
    

    

    for z in z_values:
        for i in range(n):
            inf = z_min +   i  *interval
            sup = z_min + (i+1)*interval
            if (inf <= z) and (z < sup):
                z_frequency_raw[i].append(z)

    for z in z_frequency_raw:
        z_frequency.append(len(z))
        
    return z_frequency, borne
    
        
    
    
          
    
#############################################################################################################################################################
#############################################################################################################################################################
###                                                                                                                                                       ###
###   INTERFACE        INTERFACE        INTERFACE        INTERFACE        INTERFACE        INTERFACE        INTERFACE        INTERFACE        INTERFACE   ###
###                                                                                                                                                       ###
#############################################################################################################################################################
#############################################################################################################################################################
def clicked_layer_height():
    val = content_layer_height.get()
    try:
        listbox_layer_height.insert(tk.END, float(val))
    except:
        print("value isn't numeric")
    entry_layer_height.delete(0, 'end')

def clicked_tolerance():
    val = content_tolerance.get()
    try:
        listbox_tolerance.insert(tk.END, float(val))
    except:
        print("value isn't numeric")
    entry_tolerance1.delete(0, 'end')
 
def delete():
	listbox_layer_height.delete(0, tk.END)
	listbox_tolerance.delete(0, tk.END)
 
def delete_selected():
	listbox_layer_height.delete(tk.ANCHOR)
	listbox_tolerance.delete(tk.ANCHOR)

def flatten_button():
    print("\n=====================================================\n")
    layer_height = []
    tolerance = []
    counter =0

    #get all values from listboxes
    while listbox_layer_height.get(counter) != '' and counter < 10:
        layer_height.append( listbox_layer_height.get(counter) )
        counter +=1

    counter =0
    while listbox_tolerance.get(counter) != '' and counter < 10:
        tolerance.append( listbox_tolerance.get(counter) )
        counter +=1

    if not( len(tolerance)>1 and len(tolerance)!=len(layer_height)):
        file_name_ = entry_file_name.get()
        print("file_name_  ",file_name_)
        print("layer_height",layer_height)
        print("tolerance   ",tolerance)

        flatten(file_name_,layer_height,tolerance)
    else:
        print("can't figure out which tolerance goes with which layer height")
    print(get_info(4))

def slider_changed(event):
    global nb_inter
    nb_inter_before = nb_inter
    val_slider = slider.get()
    nb_inter = int(val_slider)
    """
    entry_nb_intervalls.delete(0, 'end')
    entry_nb_intervalls.insert(0 ,str(val_slider))
    """
    if nb_inter != nb_inter_before:
        sv.set(val_slider)
        #print(val_slider)
        update_graph()

def slider_textox_changed(sv):
    global nb_inter
    global val_slider
    nb_inter_before = nb_inter
    val_text_box = (sv.get())
    try:
        nb_inter = int(val_text_box)
    except:
        print("enter an integer")

    if nb_inter != nb_inter_before:
        current_value.set(nb_inter)
        #print(val_text_box)
        update_graph()

def layer_height_textox_changed(update=True):
    global canvas
    global zero
    global borne_inv
    if update==True:
        update_graph()
    #print(borne_inv)
    lh = content_layer_height.get()
    try:
        float(lh)
    except:
        print("layer height must be a number")
    else:
        lh = float(lh)
        graph_size = (zero[1]-10)
        cell_height = graph_size/nb_inter
        value_plane = borne_inv[0] - borne_inv[-1]
        scale = value_plane/graph_size
        scale = graph_size/value_plane
        real_height = (lh - borne_inv[-1])
        
        
        #y_grad = cell_height * lh +10
        px = val_to_px(lh)
        print("px:",px)
        
        #canvas.create_line ((zero[0], y_grad), (500, y_grad), fill="blue", width=2)
        canvas.create_line ((zero[0], px), (500, px), 
                            fill="green", width=2)

        if CheckVar1.get() == 0: #asymetrical
            tolp = content_tolerance1.get()
            tolm = content_tolerance2.get()

            try:
                float(tolp)
            except:
                print("+ tolerance must be a number")
            else:
                try:
                    float(tolm)
                except:
                    print("- tolerance must be a number")
                else:
                    tolp = float(tolp)
                    tolm = float(tolm)

                    pxp = val_to_px(lh+tolp)
                    pxm = val_to_px(lh-tolm)

                    canvas.create_rectangle ((zero[0], pxp), (zero[1], pxm),
                                             outline="blue", width=1)
            
            
        else: #symetrical
            tol = content_tolerance1.get()
            
            try:
                float(tol)
            except:
                print("± tolerance must be a number")
            else:
                tol = float(tol)

                pxp = val_to_px(lh+tol)
                pxm = val_to_px(lh-tol)

                canvas.create_rectangle ((zero[0], pxp), (zero[1], pxm),
                                         outline="blue", width=1)
                
def val_to_px(val, offset=10):
    global zero
    global borne_inv
    graph_size = (zero[1]-offset)
    cell_height = graph_size/nb_inter
    value_plane = borne_inv[0] - borne_inv[-1]
    scale = graph_size/value_plane
    real_height = (val - borne_inv[-1])

    px = (value_plane-real_height) * scale +offset
    return px
    
    



def draw_samples (canvas):
    canvas.create_rectangle ((100, 100), (600, 600),  
                             fill="cyan", outline="blue", width=5)

    canvas.create_oval ((100, 100), (600, 600), 
                        fill="pink", outline="red", width=3)

    canvas.create_line ((100, 100), (500, 200),(600, 600), 
                        fill="gray", width=3, dash=(8,4))

    canvas.create_line ((100, 100), (500, 200), (600, 600), 
                        fill="black", width=5, smooth=True,
                        arrow="last", arrowshape=(30,45,15))
 
    canvas.create_text (600, 100, text= "Hello\nEverybody",
                        fill= "black", font= ("courier", 30, "bold italic"),
                        anchor="center", justify= "center")

def button_open_file():
    open_file()
    update_graph()
    
def update_graph():
    global canvas
    global z_values
    global zero
    global borne_inv
    print("nb_inter:",nb_inter)
    if len(z_values) != 0:
        z_frequency, borne = get_info(nb_inter)
        z_frequency_inv = z_frequency[::-1]
        borne_inv = borne[::-1]

        zfmax = max(z_frequency)
    
    canvas.delete("all")
    zero = [40,380]
    
    #background
    canvas.create_rectangle ((2, 2), (150, 400),  
                             fill="white", outline="blue", width=0)

    if nb_inter <= 35:
        font_size = int(9)
    elif nb_inter <= 45:
        font_size = int(8)
    elif nb_inter <= 50:
        font_size = int(7)
    elif nb_inter <= 60:
        font_size = int(6) 
    else: #nb_inter <= 65
        font_size = int(5)

    graduation = []
    nb_inter_1 = nb_inter + 1
    for i in range(nb_inter_1):
        y_grad = (zero[1]-10)/nb_inter * i +10
        y_grad1 = (zero[1]-10)/nb_inter * (i+1) +10
        graduation.append( y_grad )

        

        if len(z_values) != 0:
            if i < nb_inter:
                #red bars
                size = z_frequency_inv[i]/zfmax * (150-zero[0]) + (zero[0])
                canvas.create_rectangle ((zero[0], y_grad), (size, y_grad1),  
                                     fill="red", outline="grey", width=1)

            #anotations:
            if y_grad != zero[1]:
                canvas.create_text (15, y_grad, text= str(round(borne_inv[i],2)),
                                fill= "black", font= ("courier", font_size, "bold italic"),
                                anchor="center", justify= "center")
            else:
                canvas.create_text (15, y_grad+7, text= str(round(borne_inv[i],2)),
                            fill= "black", font= ("courier", font_size, "bold italic"),
                            anchor="center", justify= "center")
        else:
            #grid
            canvas.create_line ((zero[0]-2, y_grad), (150, y_grad), fill="grey", width=1)

    #axes
    canvas.create_line ((zero[0], 400), (zero[0], 2), 
                        fill="black", width=2)
    canvas.create_line ((0, zero[1]), (150, zero[1]), 
                        fill="black", width=2)
    layer_height_textox_changed(update=False)

def symcheck():
    C2.toggle()
    #.config(state = 'normal')
    label3_tolerance2.config(state = 'disabled')
    entry_tolerance2.config(state = 'disabled')
    tolerance1.set("±                                           mm")
    tolerance2.set("                                              mm")
    layer_height_textox_changed()

def asymcheck():
    C1.toggle()
    label3_tolerance2.config(state = 'normal')
    entry_tolerance2.config(state = 'normal')
    #.config(state = 'disabled')
    tolerance1.set("+                                           mm")
    tolerance2.set("-                                            mm")
    layer_height_textox_changed()

nb_inter = 4

info = [[] ,    []  ,     []   ,    []   ]
#info: [ 1 | z value | + value | - value ]



height = 550
width = 550
size = 'x'.join([str(width),str(height)])

root = tk.Tk()
root.title("ASCII stl flattener")
root.geometry(size)
#root.resizable(False, False)

#=========================================================================================================================#
#       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL       LABEL #
#=========================================================================================================================#

layer_height = tk.StringVar()
layer_height.set("target z height (mm)")
label1_layer_height = tk.Label( textvariable = layer_height)
label1_layer_height.pack()
label1_layer_height.place(x=52,y=40)

tolerance1 = tk.StringVar()
tolerance1.set("±                                           mm")
label2_tolerance1 = tk.Label( textvariable = tolerance1)
label2_tolerance1.pack()
label2_tolerance1.place(x=38,y=100)

tolerance2 = tk.StringVar()
tolerance2.set("                                              mm")
label3_tolerance2 = tk.Label( textvariable = tolerance2, state='disabled')
label3_tolerance2.pack()
label3_tolerance2.place(x=38,y=120)

#=========================================================================================================================#
#       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX       TEXT BOX #
#=========================================================================================================================#

# The entry to input the items
file_name = tk.StringVar()
entry_file_name = tk.Entry(root, textvariable=tk.StringVar(), width =150)
#entry_file_name.insert(0,'C:/Users/ecreach/Documents/python/maillage_structure_interne_2_evider_reduced.stl')
entry_file_name.insert(0,'C:/Users/ecreach/Documents/python/piece_test.stl')
entry_file_name.pack()

content_layer_height = tk.StringVar()
content_layer_height.trace("w", lambda name, index, mode, sv=content_layer_height: layer_height_textox_changed())
entry_layer_height = tk.Entry(root, textvariable=content_layer_height)
entry_layer_height.pack()
entry_layer_height.place(x=50,y=70)

content_tolerance1 = tk.StringVar()
content_tolerance1.trace("w", lambda name, index, mode, sv=content_tolerance1: layer_height_textox_changed())
entry_tolerance1 = tk.Entry(root, textvariable=content_tolerance1)
entry_tolerance1.pack()
entry_tolerance1.place(x=50,y=100)

content_tolerance2 = tk.StringVar()
content_tolerance2.trace("w", lambda name, index, mode, sv=content_tolerance2: layer_height_textox_changed())
entry_tolerance2 = tk.Entry(root, textvariable=content_tolerance2, state='disabled')
entry_tolerance2.pack()
entry_tolerance2.place(x=50,y=120)

sv = tk.StringVar()
sv.trace("w", lambda name, index, mode, sv=sv: slider_textox_changed(sv)) #https://stackoverflow.com/questions/6548837/how-do-i-get-an-event-callback-when-a-tkinter-entry-widget-is-modified
entry_nb_intervalls = tk.Entry(root, textvariable=sv, width =5)
entry_nb_intervalls.insert(0 ,str(nb_inter))
entry_nb_intervalls.pack()
entry_nb_intervalls.place(x=440,y=480)

#=========================================================================================================================#
#       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON       BUTTON    #
#=========================================================================================================================#

# The button to insert the item in the list
button_layer_height = tk.Button(root, text="Add Item", command=clicked_layer_height)
button_layer_height.pack()
button_layer_height.place(x=80,y=130)

button_tolerance = tk.Button(root, text="Add Item", command=clicked_tolerance)
button_tolerance.pack()
button_tolerance.place(x=250,y=900)
 
# the button to delete everything
button_delete = tk.Button(text="Delete everything", command=delete)
button_delete.pack()
button_delete.place(x=145,y=150)
 
# The button to delete only the selected item in the list
button_delete_selected = tk.Button(text="Delete Selected", command=delete_selected)
button_delete_selected.pack()
button_delete_selected.place(x=150,y=150)

# the button to flatten the stl
button_delete = tk.Button(text="Flatten ASCII stl", command=flatten_button)
button_delete.pack()
button_delete.place(x=152,y=450)

button_open = tk.Button(text="Open file", command=button_open_file)
button_open.pack()
button_open.place(x=400,y=20)
#=========================================================================================================================#
#       LISTBOX       LISTBOX       LISTBOX       LISTBOX       LISTBOX       LISTBOX       LISTBOX       LISTBOX         #
#=========================================================================================================================#
# The listbox
listbox_layer_height = tk.Listbox(root)
#listbox_layer_height.pack()
#listbox_layer_height.place(x=50,y=180)

listbox_tolerance = tk.Listbox(root)
#listbox_tolerance.pack()
#listbox_tolerance.place(x=220,y=180)

listbox_layer_height_tolerance = tk.Listbox(root, width=2)
listbox_layer_height_tolerance.pack()
listbox_layer_height_tolerance.place(x=50,y=180)



#=========================================================================================================================#
#       SLIDER       SLIDER       SLIDER       SLIDER       SLIDER       SLIDER       SLIDER       SLIDER       SLIDER    #
#=========================================================================================================================#
#https://www.pythontutorial.net/tkinter/tkinter-slider/

current_value = tk.DoubleVar()
current_value.set(nb_inter)
slider = tk.Scale(
    root,
    from_=1,
    to=100,
    orient='horizontal',
    variable=current_value,
    command=slider_changed
)
slider.pack()
slider.place(x=400,y=435)


#=========================================================================================================================#
#       CANVAS       CANVAS       CANVAS       CANVAS       CANVAS       CANVAS       CANVAS       CANVAS       CANVAS    #
#=========================================================================================================================#
canvas=tk.Canvas(root, width=150, height=400, bg="white")
canvas.pack()
canvas.place(x=350,y=50)


#=========================================================================================================================#
#       CHECKBUTTON       CHECKBUTTON       CHECKBUTTON       CHECKBUTTON       CHECKBUTTON       CHECKBUTTON             #
#=========================================================================================================================#

CheckVar1 = tk.IntVar()
CheckVar1.set(1)
C1 = tk.Checkbutton(root, text = "symetrical", variable = CheckVar1,
                 onvalue = 1, offvalue = 0, command = symcheck)
C1.pack()
C1.place(x=220,y=55)

CheckVar2 = tk.IntVar()
C2 = tk.Checkbutton(root, text = "asymetrical", variable = CheckVar2,
                 onvalue = 1, offvalue = 0, command = asymcheck)
C2.pack()
C2.place(x=220,y=75)


update_graph()


root.mainloop()
