import matplotlib.pyplot as plt
import numpy as np
def graphique_qui_ce_met_a_jour(nouv_x, nouv_y, info=[],
                                label_x="x", label_y="y", title="Title", point = False, grid = False, style_='fast',
                                x_min=False, x_max=False, y_min=False, y_max=False, tpause=1e-20,
                                x_follow=False, x_right=1, x_left=10, y_follow=False, y_right=10, y_left=10):
    if info == []: #première itération de la boucle
        list_x = np.array([nouv_x])
        list_y = np.array([nouv_y])
        fig, ax = plt.subplots()
        plt.style.use(style_)
        if point:
            line = ax.plot(list_x,list_y,'-o')
        else:
            line = ax.plot(list_x,list_y,'-')
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.title(title)

        x_window_size_constant = True
        if x_min == False and x_max == False:
            x_min = min(list_x)
            x_max = max(list_x)
            if x_max == x_min:
                x_max += 1
            x_window_size_constant = False
            #x_max += (x_max - x_min)/10
        y_window_size_constant = True
        if y_min == False and y_max == False:
            y_min = min(list_x)
            y_max = max(list_x)
            if y_max == y_min:
                y_max += 1
            y_window_size_constant = False
            #y_max += (x_max - x_min)/10

        if x_follow == True:
            x_min = nouv_x - x_left 
            x_max = nouv_x + x_right
        if y_follow == True:
            y_min = nouv_y - y_left
            y_max = nouv_y + y_right
            plt.ylim(y_min,y_max)

        plt.xlim(x_min,x_max)
        
        if grid:
            plt.grid()
        plt.ion()   # set interactive mode
        fig.show()

    else:
        plt.cla() #clears the plot to not stack up multiple curves
        plt.style.use(style_)
        
        list_x = info[0]
        list_y = info[1]
        fig = info[2]
        ax = info[3]
        label_x = info[4]
        label_y = info[5]
        title = info[6]
        tpause = info[7]
        x_window_size_constant = info[8]
        y_window_size_constant = info[9]
        x_min = info[10]
        x_max = info[11]
        y_min = info[12]
        y_max = info[13]
        grid = info[14]

        if x_window_size_constant == False:
            x_min = min(list_x)
            x_max = max(list_x)
            x_max += (x_max - x_min)/10
            if x_max == x_min:
                x_max += 1
                
        if x_follow == True:
            x_min = nouv_x - x_left
            x_max = nouv_x + x_right

        if y_follow == True:
            y_min = nouv_y - y_left
            y_max = nouv_y + y_right
            plt.ylim(y_min,y_max)
        
        list_x=np.append(list_x,nouv_x)
        list_y=np.append(list_y, nouv_y)
        #plt.cla() #clears the plot to not stack up multiple curves
        #plt.style.use(style_)
        if point:
            line = ax.plot(list_x,list_y,'-o')
        else:
            line = ax.plot(list_x,list_y,'-')
        
        plt.xlabel(label_x)
        plt.ylabel(label_y)
        plt.title(title)
        plt.xlim(x_min,x_max)

        if grid:
            plt.grid()
        
        
        fig.canvas.draw()
        plt.pause(tpause)
        
    #code à mettre avant l'appel de cette fonction :
    """
    info = []
    """
    info = [list_x, list_y, fig, ax, label_x, label_y, title, tpause, x_window_size_constant, y_window_size_constant, x_min, x_max, y_min, y_max, grid]
    return info

def test():
    tstep = 0.1
    t=0
    y=0
    inf = graphique_qui_ce_met_a_jour(t, y)
    for i in range(int(200)):
        
        y = np.sin( t )
        t += tstep

        inf = graphique_qui_ce_met_a_jour(t, y, info=inf,point = True, grid = True, x_follow=True)#,y_follow=True)
