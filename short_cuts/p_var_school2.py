# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 18:09:03 2014

@author: elias
"""

import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import math as ma

def short_cuts(g, p, k):
    enlaces=nx.edges(g)
    nodos=nx.nodes(g)
    for i in range(len(enlaces)):
        if random.random()<p[k]:
            u=random.choice(nodos)
            v=random.choice(nodos)
            while u==v or g.has_edge(u,v):
                v=random.choice(nodos)
            g.add_edge(u,v)
            g.remove_edge(*enlaces[i])

n=226
s=9.
ns=n/s
ps=(1970/226.0)/(24)
ps2=(1970/226.0)/(25)

#Análisis de 51 graphos formados aleatoriamente
print 'Frienship Networkx School 2'
#Probabilidad de shortcut:
p=np.linspace(0,1, 101)

vectorz1=np.zeros(len(p))
vectorz2=np.zeros(len(p))
vectorc=np.zeros(len(p))
logvectorc=np.zeros(len(p))

for k in range(len(p)):
    s1=nx.erdos_renyi_graph(25,ps)
    s2=nx.erdos_renyi_graph(25,ps)
    s3=nx.erdos_renyi_graph(25,ps)
    s4=nx.erdos_renyi_graph(25,ps)
    s5=nx.erdos_renyi_graph(25,ps)
    s6=nx.erdos_renyi_graph(25,ps)
    s7=nx.erdos_renyi_graph(25,ps)
    s8=nx.erdos_renyi_graph(25,ps)
    s9=nx.erdos_renyi_graph(26,ps2)
    esc= nx.disjoint_union_all([s1,s2,s3,s4,s5,s6,s7,s8,s9])
    
    #Se aplican shortcuts para la red de toda la escuela
    short_cuts(esc,p,k)

    #Matriz de adyacencia: paso de igraph a networkx
    m=nx.adjacency_matrix(esc)
    
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
    
    #Más propiedades de la red
    clustering=nx.average_clustering(esc)
    vectorc[k]=clustering
    logvectorc[k]=ma.log(clustering)
    print '%1.2f: %1.8f, %3.8f, %3.8f' %(p[k], vectorz1[k], vectorz2[k], vectorc[k])

plt.subplot(3,1,2)
#plt.xlabel("p", fontsize=16)
plt.ylabel(r"$\'Indice \ de \ Clustering$", fontsize=12)
plt.axhline(y=0.248,color='k',linestyle='steps--')
plt.axvline(x=0.145,color='k',linestyle='steps--')
#plt.title('Clustering index', fontsize=18)
plt.text(0.95,0.32,"b", fontsize=10, color="black")
plt.tick_params(axis='both', which='major', labelsize=10)
plt.plot(p,vectorc,'ob', p,vectorc,'g')