import math
import random

def rand_start(n,maxi, typ="int"):
    liste = []
    for i in range(int(n)):
        if typ == 'int':
            liste.append( int(random.random() * maxi +1 ))
            target = int(random.random() * maxi +1 )
        else:
            liste.append( random.random() * maxi )
            target = random.random() * maxi
    
    return liste, target
        
