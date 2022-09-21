# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 15:56:13 2014

@author: elias
"""

import networkx as nx
import igraph as ig
import numpy as np
import random
#import matplotlib.pyplot as plt
def short_cuts(g, p):
    enlaces=g.get_edgelist()
    nodos=np.arange(g.vcount())
    for i in range(len(enlaces)):
        if random.random()<p:
            u=random.choice(nodos)
            v=random.choice(nodos)
            while u==v or g.are_connected(u,v):
                v=random.choice(nodos)
            g.add_edges((u,v))
            g.delete_edges(g.get_eid(*enlaces[i]))
            

n=108
s=6.
ns=n/s
ps=9.3148148148/(ns-1)

p=0.216770816174
#p=0.217654694937
paso=100

x=np.arange(1,paso+1)
vectorz1=np.zeros(len(x))
vectorz2=np.zeros(len(x))
vectorc=np.zeros(len(x))
for k in range(paso):
    #Subredes representando a cada salón
    s1=ig.Graph.Erdos_Renyi(18,ps)
    s2=ig.Graph.Erdos_Renyi(18,ps)
    s3=ig.Graph.Erdos_Renyi(18,ps)
    s4=ig.Graph.Erdos_Renyi(18,ps)
    s5=ig.Graph.Erdos_Renyi(18,ps)
    s6=ig.Graph.Erdos_Renyi(18,ps)
    
    #La red entera formada por todos los salones
    esc=s1+s2+s3+s4+s5+s6
    
    short_cuts(esc,p)

    #Matriz de adyacencia
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

#Resultados
print 'Frienship Networkx School 1'
print 'Promedio de Clustering', np.sum(vectorc)/paso
print 'Promedio de z1', np.sum(vectorz1)/paso
print 'Promedio de z2', np.sum(vectorz2)/paso