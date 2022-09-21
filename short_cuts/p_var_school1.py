# -*- coding: utf-8 -*-
"""
Created on Sat Jun 14 17:57:16 2014

@author: elias
"""

import networkx as nx
import igraph as ig
import numpy as np
import random
import matplotlib.pyplot as plt
import math as ma

def short_cuts(g, p, k):
    enlaces=g.get_edgelist()
    nodos=np.arange(g.vcount())
    for i in range(len(enlaces)):
        if random.random()<p[k]:
            u=random.choice(nodos)
            v=random.choice(nodos)
            while u==v or g.are_connected(u,v):
                v=random.choice(nodos)
            g.add_edges((u,v))
            g.delete_edges(g.get_eid(*enlaces[i]))
            

n=108
s=6
ns=n/s
ps=9.3148148148/(ns-1)

#Análisis de 51 graphos formados aleatoriamente
print 'Frienship Networkx School 1'
print 'probabilidad, z1    , z2    , clustering'
#Probabilidad de shortcut:
p=np.linspace(0,1, 51)
vectorz1=np.zeros(len(p))
vectorz2=np.zeros(len(p))
vectorc=np.zeros(len(p))
logvectorc=np.zeros(len(p))

for k in range(len(p)):
    #Subredes representando a cada salón
    s1=ig.Graph.Erdos_Renyi(18,ps)
    s2=ig.Graph.Erdos_Renyi(18,ps)
    s3=ig.Graph.Erdos_Renyi(18,ps)
    s4=ig.Graph.Erdos_Renyi(18,ps)
    s5=ig.Graph.Erdos_Renyi(18,ps)
    s6=ig.Graph.Erdos_Renyi(18,ps)
    
    #La red entera formada por todos los salones
    esc=s1+s2+s3+s4+s5+s6
    
    short_cuts(esc,p,k)

    #Matriz de adyacencia: cambio de igraph a networkx
    m=np.array(list(esc.get_adjacency()))
    escuela=nx.from_numpy_matrix(m)
    
    #Caminos de longitud 1
    l1= np.sum(m, dtype=float)
    z1a=l1/n
    vectorz1[k]=z1a
    
    #Caminos de longitud 2
    m2=np.dot(m,m)
    for i in xrange(n):
        m2[i,i]=0
        for j in xrange(n):
            if m2[i,j]>0:
                m2[i,j]=1
            if m[i,j]==1:
                m2[i,j]=0

    l2=np.sum(m2, dtype=float)
    z2a=l2/n
    vectorz2[k]=z2a
    
    #Propiedades de la red
    clustering=nx.average_clustering(escuela)  
    vectorc[k]=clustering
    logvectorc[k]=ma.log(clustering)
    print 'p=%1.2f: %1.8f, %3.8f, %3.8f' %(p[k], vectorz1[k], vectorz2[k], vectorc[k])
    
#plt.plot(p,vectorz1,'o',p,vectorz1,'r')
plt.plot(p,logvectorc,'o',p,logvectorc,'r')