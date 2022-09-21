# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 17:16:08 2014

@author: elias
"""

import networkx as nx
import igraph as ig
import numpy as np
import random

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
#probabilidad de shortcut:
p=0.235

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
#Más propiedades de la red
orden=escuela.order()
clustering=nx.average_clustering(escuela)

#Resultados
print 'Frienship Networkx School 1'
print 'z1', z1a
print 'z2', z2a
print 'Orden:', orden
print 'Clustering promedio:', clustering
print 'Umbral:', l1/l2