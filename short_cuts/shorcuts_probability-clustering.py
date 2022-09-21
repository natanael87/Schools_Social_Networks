# -*- coding: utf-8 -*-

import networkx as nx
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import math as ma

def short_cuts(g, p, k):
    enlaces=nx.edges(g)
    nodos=nx.nodes(g)
    for i in range(len(enlaces)):
        if rd.random()<p[k]:
            u=rd.choice(nodos)
            v=rd.choice(nodos)
            while u==v or g.has_edge(u,v):
                v=rd.choice(nodos)
            g.add_edge(u,v)
            g.remove_edge(*enlaces[i])
            

n=108
s=6
ns=n/s
ps=9.3148148148/(ns-1)

#Análisis de 51 grafos formados aleatoriamente
print 'Probability     z1             z2         Clustering'
#Probabilidad de shortcut:
p=np.linspace(0,1, 101)
vectorz1=np.zeros(len(p))
vectorz2=np.zeros(len(p))
vectorc=np.zeros(len(p))
logvectorc=np.zeros(len(p))

for k in range(len(p)):
    #Subredes representando a cada salón
    s1=nx.erdos_renyi_graph(18,ps)
    s2=nx.erdos_renyi_graph(18,ps)
    s3=nx.erdos_renyi_graph(18,ps)
    s4=nx.erdos_renyi_graph(18,ps)
    s5=nx.erdos_renyi_graph(18,ps)
    s6=nx.erdos_renyi_graph(18,ps)
    
    #La red entera formada por todos los salones
    esc=nx.disjoint_union_all([s1,s2,s3,s4,s5,s6])
    
    short_cuts(esc,p,k)

    #Matriz de adyacencia: cambio de igraph a networkx
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
    
    #Propiedades de la red
    clustering=nx.average_clustering(esc)  
    vectorc[k]=clustering
    logvectorc[k]=ma.log(clustering)
    print 'p=%1.2f:     %1.8f,    %3.8f,    %3.8f'%(p[k], vectorz1[k], vectorz2[k], vectorc[k])
    
plt.subplot(3,1,1)
#plt.xlabel("p", fontsize=16)
#plt.ylabel("Clustering index", fontsize=16)
plt.axhline(y=0.292,color='k',linestyle='steps--')
plt.axvline(x=0.235,color='k',linestyle='steps--')
plt.title(r"$Variaci\'on \ del \ \'Indice \ de \ Clustering$", fontsize=12)
plt.text(0.95,0.5,"a", fontsize=10, color="black")
plt.tick_params(axis='both', which='major', labelsize=10)
plt.plot(p,vectorc, 'ob' , p,vectorc,'g')

#plt.figure(2)
#plt.xlabel("p", size=15)
#plt.ylabel("$z_1/z_{2}$", size=18)
#plt.axhline(y=0.218,color='r',linestyle='steps--')
#plt.axvline(x=0.235,color='r',linestyle='steps--')
#plt.text(0.180,0.175,r"$(0.235,0.218)$", fontsize=12, color="black")
#plt.plot(p,vectorz1/vectorz2,'o',p,vectorz1/vectorz2,'r')