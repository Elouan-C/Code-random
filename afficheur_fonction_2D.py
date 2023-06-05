"""
     PARAMETRES UTILISATEUR
"""
#Resolution:
res_a = 0.01
res_y = 0.1

#Etendue:
et_a =[0,60]
et_y =[-360,0]

Ye = -10

R = 5

g = 9.81

dpi = 1000


import math
import numpy as np
import matplotlib.pyplot as plt

def fonction(a,y,ye,r,g=9.81):
    #Parametres:
    pi = math.pi

    a = np.radians(a)
    
    ans = pi/2 -(
        np.arcsin( ( (2*r*g+2*y*ye)/(2*(y-r))-y ) / (g**2*np.cos(a)**2 + (g*np.sin(a)-y)**2)**0.5 ) ) - (
            np.arctan( g*np.cos(a) / (g*np.sin(a)-y) ))

    return ans

fig = plt.figure()
ax = fig.add_subplot(111)


a = np.arange(et_a[0], et_a[1], res_a)
y = np.arange(et_y[0], et_y[1], res_y)
aa, yy = np.meshgrid(y, a, sparse=True)
b = fonction(aa,yy, Ye, R, g) #calcule de toutes les valeurs
etendu = [et_a[0], et_a[1] , et_y[0], et_y[1]]

ax.set_xlabel('$Y_{F}$')
ax.set_ylabel(r'$\alpha$')
ax.set_title(r'$\beta$')
pcm = ax.pcolormesh(y,a,b)
ax.set_aspect('auto')
plt.gca().invert_xaxis()
fig.colorbar(pcm, ax=ax)
fig.savefig('schéma.png',dpi=dpi,format='png')
plt.show()
