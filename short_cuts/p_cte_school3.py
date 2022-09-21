# -*- coding: utf-8 -*-
"""
Created on Sun Jun 15 19:59:08 2014

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
            

n=419
s=9.
ns=n/s
ps=(1970/226.0)/(ns-1)

ns=419/12
pf=2*s*(3150/419.0)/(419-2*12.0)

p=0.23051

print 'Frienship Networkx School 2'
#Se aplica la iteración
paso=50

x=np.arange(1,paso+1)
vectorz1=np.zeros(len(x))
vectorz2=np.zeros(len(x))
vectorc=np.zeros(len(x))

for k in range(paso):
    #Salon 1
    f1=ig.Graph.Erdos_Renyi(18,pf)
    f2=ig.Graph.Erdos_Renyi(17,pf)
    s1=f1+f2
    short_cuts(s1,p)

    #Salón 2
    f3=ig.Graph.Erdos_Renyi(18,pf)
    f4=ig.Graph.Erdos_Renyi(17,pf)
    s2=f3+f4
    short_cuts(s2,p)
    
    #Salón 3
    f5=ig.Graph.Erdos_Renyi(18,pf)
    f6=ig.Graph.Erdos_Renyi(17,pf)
    s3=f5+f6
    short_cuts(s3,p)
            
    #Salón 4
    f7=ig.Graph.Erdos_Renyi(18,pf)
    f8=ig.Graph.Erdos_Renyi(17,pf)
    s4=f7+f8
    short_cuts(s4,p)

    #Salón 5
    f9=ig.Graph.Erdos_Renyi(18,pf)
    f10=ig.Graph.Erdos_Renyi(17,pf)
    s5=f9+f10
    short_cuts(s5,p)
    
    #Salón 6        
    f11=ig.Graph.Erdos_Renyi(18,pf)
    f12=ig.Graph.Erdos_Renyi(17,pf)
    s6=f11+f12
    short_cuts(s6,p)
    
    #Salón 7
    f13=ig.Graph.Erdos_Renyi(18,pf)
    f14=ig.Graph.Erdos_Renyi(17,pf)
    s7=f13+f14
    short_cuts(s7,p)
    
    #Salón 8
    f15=ig.Graph.Erdos_Renyi(18,pf)
    f16=ig.Graph.Erdos_Renyi(17,pf)
    s8=f15+f16
    short_cuts(s8,p)
    
    #Salón 9
    f17=ig.Graph.Erdos_Renyi(18,pf)
    f18=ig.Graph.Erdos_Renyi(17,pf)
    s9=f17+f18
    short_cuts(s9,p)
    
    #Salón 10
    f19=ig.Graph.Erdos_Renyi(18,pf)
    f20=ig.Graph.Erdos_Renyi(17,pf)
    s10=f19+f20
    short_cuts(s10,p)
    
    #salón 11
    f21=ig.Graph.Erdos_Renyi(17,pf)
    f22=ig.Graph.Erdos_Renyi(18,pf)
    s11=f21+f22
    short_cuts(s11,p)
    
    #Salón 12   
    f23=ig.Graph.Erdos_Renyi(17,pf)
    f24=ig.Graph.Erdos_Renyi(17,pf)
    s12=f23+f24
    short_cuts(s12,p)
    
    #Se aplican shortcuts a la red formada por el conjunto de salones
    esc=s1+s2+s3+s4+s5+s6+s7+s8+s9+s10+s11+s12
    short_cuts(esc,p) 
            
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
    l2=np.sum(m2,dtype=float)
    z2a=l2/n
    vectorz2[k]=z2a

    #Más propiedades de la red
    orden=escuela.order()
    clustering=nx.average_clustering(escuela)
    vectorc[k]=clustering
    print '.',

#Resultados
print
print 'Promedio de z1', np.sum(vectorz1)/paso
print 'Promedio de z2', np.sum(vectorz2)/paso
print 'Promedio de Clustering', np.sum(vectorc)/paso