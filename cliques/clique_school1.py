# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 11:46:22 2014

@author: elias
"""

import numpy as np
import networkx as nx
import igraph as ig
#import matplotlib.pyplot as plt

#Cargar la matriz de encuestas
a=np.loadtxt('esc1.txt',dtype=float)

s =6 #Número de salones

#Convertir datos a relaciones de amistad 
n=a[0].size

for i in xrange(n):
    for j in xrange(n):
        if a[i,j]==5.0 or a[i,j]==6.0 or a[i,j]==2.0:
            a[i,j]=0.0
        elif a[i,j]==3.0 or a[i,j]==4.0:
            a[i,j]=1.0
               
################## Método 1
#Caminos de longitud 1
l1=a.sum()
z1=l1/n

#Caminos de longitud 2
a2=np.dot(a,a)
for i in xrange(n):
    a2[i,i]=0
    for j in xrange(n):
        if a2[i,j]>0:
            a2[i,j]=1
        if a[i,j]==1:
            a2[i,j]=0

l2=a2.sum()
z2=l2/n

#Transición de fase
bc=l1/l2

#Convertir a grapho
A=np.matrix(a)
G=nx.from_numpy_matrix(A)
edges=G.edges()
g=ig.Graph(edges)

#Cliques
cliques=list(nx.find_cliques(G))
cli=np.array(cliques)

#Cliques community
k=3.0
l=list(nx.k_clique_communities(G,k))
pck=1/(((k-1)*n)**(1/(k-1)))

print 'Friendship network measurements',':','School 1'
print '-Total de comunidades %d-cliqués = %d' %(k,len(l))

membership=np.ones(n, dtype= int)
if len(l)!=0:
    tam=np.zeros(len(l))
    print '-El tamaño de cada comunidad es:'     
    ini=0
    for i in range(len(l)):
        tam[i]=len(l[i])
        membership[ini:tam[i]+ini]=membership[ini:tam[i]+ini]*i
        ini+=tam[i]
        print '[%d]: %d'%(i,len(l[i]))
        print 'Los nodos incluidos son:',list(l[i])
    print
    Phi=np.ma.max(tam)/n
    print 'Tamaño de la comunidad mayor:', np.ma.max(tam)
    print 'Tamaño relativo del cluster máximo:', Phi
else:
    Phi=0
    print '-No se encontraron cliqués de tamaño %d' %(k)
print 'p crítico: %f' % (pck)
print 'p medido:', z1/n
print 'p medido/p crítico:', z1/(pck*n)
#print g.community_walktrap().as_clustering()
#print g.community_label_propagation()

#Coloreando el componente más grande
zc_1=0.0
colors=['cyan']*n
if Phi>0:
    for i in range(len(list(l[0]))):
        colors[list(l[0])[i]]='red'
        zc_1+=G.degree( list(l[0])[i])
        print list(l[0])[i], G.degree(list(l[0])[i])
    print tam
    print zc_1/np.ma.max(tam)
    
nx.draw_spring(G, node_color=colors )