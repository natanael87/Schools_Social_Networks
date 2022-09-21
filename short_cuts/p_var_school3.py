# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 03:26:38 2014

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
            

n=419
s=12.
ns=n/s
ps=(1970/226.0)/(ns-1)
ns=419/12
#Probabilidad de enlace para cada subgrupo en cada salón
pf=2*s*(3150/419.0)/(419-2*12.0)


#Análisis de 51 graphos formados por 24 grafos aleatorios
print 'Frienship Networkx School 3'
#probabilidad de los shortcuts
p=np.linspace(0,1, 101)
vectorz1=np.zeros(len(p))
vectorz2=np.zeros(len(p))
vectorc=np.zeros(len(p))
logvectorc=np.zeros(len(p))

for k in range(len(p)):
    #Salon 1
    f1=nx.erdos_renyi_graph(18,pf)
    f2=nx.erdos_renyi_graph(17,pf)
    s1=nx.disjoint_union(f1,f2)
    short_cuts(s1,p,k)

    #Salón 2
    f3=nx.erdos_renyi_graph(18,pf)
    f4=nx.erdos_renyi_graph(17,pf)
    s2=nx.disjoint_union(f3,f4)
    short_cuts(s2,p,k)
    
    #Salón 3
    f5=nx.erdos_renyi_graph(18,pf)
    f6=nx.erdos_renyi_graph(17,pf)
    s3=nx.disjoint_union(f5,f6)
    short_cuts(s3,p,k)
            
    #Salón 4
    f7=nx.erdos_renyi_graph(18,pf)
    f8=nx.erdos_renyi_graph(17,pf)
    s4=nx.disjoint_union(f7,f8)
    short_cuts(s4,p,k)

    #Salón 5
    f9=nx.erdos_renyi_graph(18,pf)
    f10=nx.erdos_renyi_graph(17,pf)
    s5=nx.disjoint_union(f9,f10)
    short_cuts(s5,p,k)
    
    #Salón 6        
    f11=nx.erdos_renyi_graph(18,pf)
    f12=nx.erdos_renyi_graph(17,pf)
    s6=nx.disjoint_union(f11,f12)
    short_cuts(s6,p,k)
    
    #Salón 7
    f13=nx.erdos_renyi_graph(18,pf)
    f14=nx.erdos_renyi_graph(17,pf)
    s7=nx.disjoint_union(f13,f14)
    short_cuts(s7,p,k)
    
    #Salón 8
    f15=nx.erdos_renyi_graph(18,pf)
    f16=nx.erdos_renyi_graph(17,pf)
    s8=nx.disjoint_union(f15,f16)
    short_cuts(s8,p,k)
    
    #Salón 9
    f17=nx.erdos_renyi_graph(18,pf)
    f18=nx.erdos_renyi_graph(17,pf)
    s9=nx.disjoint_union(f17,f18)
    short_cuts(s9,p,k)
    
    #Salón 10
    f19=nx.erdos_renyi_graph(18,pf)
    f20=nx.erdos_renyi_graph(17,pf)
    s10=nx.disjoint_union(f19,f20)
    short_cuts(s10,p,k)
    
    #salón 11
    f21=nx.erdos_renyi_graph(18,pf)
    f22=nx.erdos_renyi_graph(17,pf)
    s11=nx.disjoint_union(f21,f22)
    short_cuts(s11,p,k)
    
    #Salón 12   
    f23=nx.erdos_renyi_graph(17,pf)
    f24=nx.erdos_renyi_graph(17,pf)
    s12=nx.disjoint_union(f23,f24)
    short_cuts(s12,p,k)
    
    #Se aplican shortcuts a la red formada por el conjunto de 12 salones
    esc=nx.disjoint_union_all([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12])
    short_cuts(esc,p,k) 
    
    #Matriz de adjacencia:
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
    l2=np.sum(m2,dtype=float)
    z2a=l2/n
    vectorz2[k]=z2a
    #Más propiedades de la red
    orden=esc.order()
    clustering=nx.average_clustering(esc)
    vectorc[k]=clustering
    logvectorc[k]=ma.log(clustering)
    print 'p=%1.2f: %1.8f, %3.8f, %3.8f' %(p[k], vectorz1[k], vectorz2[k], vectorc[k])

plt.subplot(3,1,3)
plt.xlabel(r"$probabilidad \ de \ shortcut$", fontsize=12)
#plt.ylabel("C", fontsize=16)
plt.axhline(y=0.226,color='k',linestyle='steps--')
plt.axvline(x=0.15,color='k',linestyle='steps--')
#plt.title('Clustering index', fontsize=18)
plt.text(0.95,0.3,"c", fontsize=10, color="black")
plt.tick_params(axis='both', which='major', labelsize=10)
plt.plot(p,vectorc,'ob', p,vectorc,'g')