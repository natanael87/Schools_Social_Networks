# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 17:44:33 2014

@author: elias
"""

import networkx as nx
import igraph as ig
import numpy as np
import random

n=226
s=9.
ns=n/s
ps=(1970/226.0)/(24)
ps2=(1970/226.0)/25
#Probabilidad de shortcut:
p=0.145

#9 redes representando a cada salón:
s1=ig.Graph.Erdos_Renyi(25,ps)
s2=ig.Graph.Erdos_Renyi(25,ps)
s3=ig.Graph.Erdos_Renyi(25,ps)
s4=ig.Graph.Erdos_Renyi(25,ps)
s5=ig.Graph.Erdos_Renyi(25,ps)
s6=ig.Graph.Erdos_Renyi(25,ps)
s7=ig.Graph.Erdos_Renyi(25,ps)
s8=ig.Graph.Erdos_Renyi(25,ps)
s9=ig.Graph.Erdos_Renyi(26,ps2)
#La red formada por el total de 9 salones:
esc= s1+s2+s3+s4+s5+s6+s7+s8+s9

enl=esc.get_edgelist()
nod=np.arange(n)
for i in range(len(enl)):
    if random.random()<p:
        u=random.choice(nod)
        v=random.choice(nod)
        while u==v or esc.are_connected(u,v):
            v=random.choice(nod)
        esc.add_edges((u,v))
        esc.delete_edges(esc.get_eid(*enl[i]))

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
print 'Frienship Networkx School 2'
print 'z1', z1a
print 'z2', z2a
print 'Orden:', orden
print 'Clustering promedio:', clustering
print 'Umbral:', l1/l2
nx.draw(escuela)