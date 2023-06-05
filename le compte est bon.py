#https://fr.wikipedia.org/wiki/Des_chiffres_et_des_lettres#Le_compte_est_bon
import math
import random
import itertools

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
        
def nombre_cible(): #de 101 à 999
    n = int(random.random()*898 +101)
    return n

def liste_aléatoire(n = 6):
    plaques = [1,1, 2,2, 3,3, 4,4, 5,5, 6,6, 7,7, 8,8, 10,10, 25, 50, 75, 100]
    liste = random.sample(plaques,n)
    return liste

def operation(n = 6):
    liste = []
    oper = ['+', '-', '*', '/','0']
    for i in range(n):
        for a in oper:
            r=4


def toute_position_possible(l_operateur,r=5):
    n = len(l_operateur) #nombre d'élément
    obj = itertools.product(l_operateur, repeat=r)
    liste = []
    for i in obj:
        liste+=[list(i)]
    return liste

def trouver_calcule(cible, liste_num):
    l = liste_num
    #print("l:",l)
    oper = ['+', '-', '*', '/']
    nb_operations = len(l)-1
    
    OPERATEURS = toute_position_possible(oper,r=nb_operations)
    print(OPERATEURS)
    resultats = []
    i=0
    for operateur in OPERATEURS:
        #print("i:",i)
        re = l[0]
        j = 0
        for op in operateur:
            j += 1
            if op == '+':
                re += l[j]
                
            elif op == '-':
                re -= l[j]
                
            elif op == '*':
                re *= l[j]
                
            elif op == '/':
                re /= l[j]
                
            elif op == '0':
                re = l[j]

            if j == nb_operations:
                delta = abs(cible-re)
                if len(resultats) == 0:
                    resultats += [i,re,delta]
                elif delta < resultats[2]:
                    resultats[0] = i
                    resultats[1] = re
                    resultats[2] = delta
        i+=1

    liste_string =[]
    i = resultats[0]
    for j in range(nb_operations):
        liste_string.append(str(l[j]))
        liste_string.append(OPERATEURS[i][j])
    liste_string.append(str(l[-1]))
    liste_string += ['=',str(resultats[1])]
    string = ' '.join(liste_string)
    #print(string)
    return string
    
def main(n=5):
    for i in range(n):
        nb = nombre_cible()
        li = liste_aléatoire()
        resultat = trouver_calcule(nb, li)

        print('\n=====================')
        print(li)
        print("cible:",nb)
        print(resultat)
