# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 09:27:34 2014

@author: elias
"""

import numpy as np
import networkx as nx
#import matplotlib.pyplot as plt

#Cargar la matriz de encuestas
a=np.loadtxt('esc1.txt',dtype=float)

s=6 #Número de salones

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

#Análisis por salón
ns=n/s
f=(ns-1)/(2*z1)
ps=z1/(ns-1)

zB=np.zeros(s)
z2B=np.zeros(s)
size=0
for i in xrange(s):
    B1=nx.binomial_graph(ns,ps)
    m1=nx.adjacency_matrix(B1)
    size+= B1.size()
    l1B1=m1.sum()
    zB[i]=l1B1/ns
    m2=np.dot(m1,m1)
    for j in xrange(s):
        m2[j,j]=0
        for k in xrange(ns):
            if m2[j,k]>0:
                m2[j,k]=1
            if m1[j,k]==1:
                m2[j,k]=0
    l2B=m2.sum()
    z2B[i]=l2B/ns
print zB
print z2B
print
z1pro=zB.sum()/s
z2pro=z2B.sum()/s
print z1pro
print z2pro
print 

#Convertir a grapho
A=np.matrix(a)
G=nx.from_numpy_matrix(A)

#Resultados
print 'Friendship network measurements',':','School 1'
print 'Order :',G.order()
print 'Size :',G.size()
print
print 'z1:', z1
print 'z2',z2
print 'bc:', bc